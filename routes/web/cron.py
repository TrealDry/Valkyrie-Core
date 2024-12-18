from . import web
from time import time
from os.path import join
from loguru import logger
from flask import request
from hashlib import sha256
from config import REDIS_PREFIX, PATH_TO_ROOT
from routes.score.get_scores import upload_scores

from utils import database as db

from utils.redis_db import client as rd
from utils.request_get import request_get
from utils.limit_check import limit_check


CP_RATE = 1
CP_FEATURED = 2
CP_EPIC = 4
CP_LEGENDARY = 6
CP_MYTHIC = 10


def update_demon_list(levels=None):
    if levels is None:
        levels = tuple(db.level.find({"stars": {"$gt": 0}}))

    demon_levels = [i for i in levels if i["demon"] == 1]
    demon_levels_string = ";".join(
        list(map(  # level_id - demon_type - is platformer
            lambda x: f"{x["_id"]}-{x["demon_type"]}-{1 if x["length"] == 5 else 0}",
            demon_levels
        ))
    )

    rd.set(f"{REDIS_PREFIX}:all_demons", demon_levels_string)
    return True


@web.route("/cron/<task>", methods=("POST", "GET"))
def cron(task):
    logger.info("Начало работы cron!")

    if request.method != "POST":
        logger.warning("Запрос не является POST!")
        return ""

    key = request_get("master_key")

    if key == "":
        logger.warning("Ключ пустой!")
        return ""

    if db.master_key.count_documents({
        "key": sha256(key.encode("utf-8")).hexdigest(),
        "comment": "for cron"
    }) == 0:
        logger.warning("Ключ не был обнаружен!")
        return ""

    if task == "gd":
        logger.info("Тип таска был выбран 'gd'")

        """ Выдача creator points """

        creator_list = {}
        creator_logs = ""

        levels = tuple(db.level.find({"stars": {"$gt": 0}}))

        for creator in db.account_stat.find({"creator_points": {"$gt": 0}}):
            creator_list[creator["_id"]] = 0

        if len(levels) != 0:
            for lvl in levels:
                if lvl["account_id"] not in creator_list:
                    creator_list[lvl["account_id"]] = 0

                if (lvl["featured"] == 0 and lvl["epic"] == 0
                        and lvl["legendary"] == 0 and lvl["mythic"] == 0):
                    creator_list[lvl["account_id"]] += CP_RATE

                elif (lvl["featured"] == 1 and lvl["epic"] == 0
                        and lvl["legendary"] == 0 and lvl["mythic"] == 0):
                    creator_list[lvl["account_id"]] += CP_FEATURED

                elif lvl["epic"] == 1 and lvl["legendary"] == 0 and lvl["mythic"] == 0:
                    creator_list[lvl["account_id"]] += CP_EPIC

                elif lvl["legendary"] == 1 and lvl["mythic"] == 0:
                    creator_list[lvl["account_id"]] += CP_LEGENDARY

                elif lvl["mythic"] == 1:
                    creator_list[lvl["account_id"]] += CP_MYTHIC

            for creator in creator_list:
                creator_logs += f"{creator} - {creator_list[creator]} CP; "

                db.account_stat.update_one({"_id": creator}, {"$set": {
                    "creator_points": creator_list[creator]
                }})

        upload_scores("creators")
        logger.info(f"Статистика по креатор поинтам: {creator_logs}")

        del creator_list
        del creator_logs

        """ Подсчёт всех демонов """

        update_demon_list(levels)

        """ Античит """

        max_stars = 202  # Сколько можно собрать статистику, не проходя онлайн уровней
        max_moons = 25
        max_demons = 3
        max_gold_coins = 81
        max_silver_coins = 0

        users = tuple(db.account_stat.find({"is_top_banned": 0}))
        map_packs = tuple(db.map_pack.find())
        gauntlets = tuple(db.gauntlet.find())
        daily_levels = tuple(db.daily_level.find())

        for level in levels:
            if level["length"] == 5:
                max_moons += level["stars"]
            else:
                max_stars += level["stars"]
            max_demons += level["demon"]
            max_silver_coins += level["coins"] if level["is_silver_coins"] == 1 else 0

        if bool(map_packs):
            for map_pack in map_packs:
                max_stars += map_pack["stars"]
                max_gold_coins += map_pack["coins"]

        if bool(gauntlets):
            for gauntlet in gauntlets:
                level_ids = gauntlet["levels"].split(",")
                for level_id in level_ids:
                    try:
                        level = db.level.find({"_id": int(level_id)})[0]
                    except IndexError:
                        continue

                    if level["length"] == 5:
                        max_moons += level["stars"]
                    else:
                        max_stars += level["stars"]

                    max_demons += level["demon"]
                    max_silver_coins += level["coins"] if level["is_silver_coins"] == 1 else 0

        if bool(daily_levels):
            for daily_level in daily_levels:
                level_id = daily_level["level_id"]
                level = db.level.find({"_id": int(level_id)})[0]

                if level["length"] == 5:
                    max_moons += level["stars"]
                else:
                    max_stars += level["stars"]

                max_demons += level["demon"]
                max_silver_coins += level["coins"] if level["is_silver_coins"] == 1 else 0

        logger.info("Максимальное количество элементов статистики: "
            f"stars - {max_stars}; moons - {max_moons}; demons - {max_demons}; "
            f"gold_coins - {max_gold_coins}; silver_coins - {max_silver_coins}")

        for user in users:
            if not limit_check(
                (user["stars"], max_stars), (user["moons"], max_moons), (user["demons"], max_demons),
                (user["user_coins"], max_silver_coins), (user["secret_coins"], max_gold_coins)
            ):
                logger.info(f"Пользователь {user["_id"]} был забанен!")
                db.account_stat.update_one({"_id": user["_id"]}, {"$set": {
                    "is_top_banned": 1
                }})

        """ Обновление поля global_rank у игроков """

        top_list = rd.get(f"{REDIS_PREFIX}:top:top")

        if top_list is None:
            top_list = upload_scores()

        top_list = top_list.split("|")

        for i in range(1, len(top_list)):
            user = top_list[i - 1].split(":")

            db.account_stat.update_one({"_id": int(user[3])}, {"$set": {
                "global_rank": i
            }})

        """ Очистка неактивированных аккаунтов """

        db.account.delete_many({
            "is_valid": 0,
            "date": {"$lte": int(time()) - 3600}  # Есть только час на активацию
        })

        """ Если игрок лишился статуса модератора """

        for user in db.account_stat.find({"mod_badge": {"$gt": 0}}):
            if db.role_assign.count_documents({"_id": user["_id"]}) == 0:
                comment_color = user["comment_color"] if user["vip_status"] == 1 else ""
                prefix = user["prefix"] if user["prefix"] not in ("Moderator", "Elder Moderator") else ""

                db.account_stat.update_one({"_id": user["_id"]}, {"$set": {
                    "mod_badge": 0,
                    "prefix": prefix,
                    "comment_color": comment_color
                }})

        """ Обнуление rate_time, если с уровня сняли оценку """

        for level in db.level.find({"rate_time": {"gt": 0}}):
            if level["stars"] > 0:
                continue

            db.level.update_one({"_id": level["_id"]}, {"$set": {"rate_time": 0}})

        logger.success(f"Работа cron под таском '{task}' произведена успешно!")
        return "1"

    else:
        logger.warning(f"Тип таска '{task}' не был обнаружен!")
