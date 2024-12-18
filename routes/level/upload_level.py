import json
from . import level
from time import time
from os.path import join
from sys import getsizeof
from loguru import logger
from config import PATH_TO_DATABASE, PATH_TO_ROOT

from utils import database as db

from utils.last_id import last_id
from utils.regex import char_clean
from utils.passwd import check_password
from utils.limit_check import limit_check
from utils.request_get import request_get
from utils.check_secret import check_secret
from utils.check_version import check_version
from utils.plugin_manager import plugin_manager
from utils.request_limiter import request_limiter
from utils.base64_dec_and_enc import base64_decode


MAXIMUM_LEVEL_SIZE = 5 * 1024 * 1024  # 5 MB
MINIMUM_NUMBER_BLOCKS = 49

RESERVED_LEVEL_IDS = (3001, 5001, 5002, 5003, 5004)


@level.route(f"{PATH_TO_DATABASE}/uploadGJLevel21.php", methods=("POST", "GET"))
def upload_level():
    if not check_secret(
        request_get("secret"), 1
    ):
        logger.debug(f"Секретный ключ не совпал ({request_get("secret")})")
        return "-1"

    account_id = request_get("accountID", "int")
    password = request_get("gjp")

    is_gjp2 = False

    if request_get("gjp2") != "":
        is_gjp2 = True
        password = request_get("gjp2")

    if not check_password(
        account_id, password, is_gjp=not is_gjp2, is_gjp2=is_gjp2
    ):
        if account_id <= 0: logger.info("Пользователя не существует")
        else: logger.info(f"Неправильный пароль у пользователя ({account_id})")
        return "-1"

    level_name = char_clean(request_get("levelName"))
    level_string = request_get("levelString")

    extra_string = request_get("extraString") \
        if request_get("extraString") != "" else "29_29_29_40_29_29_29_29_29_29_29_29_29_29_29_29"
    level_length = request_get("levelLength", "int")  # 5 = platformer
    audio_track = request_get("audioTrack", "int")
    level_desc = request_get("levelDesc")
    two_player = request_get("twoPlayer", "int")
    unlisted = request_get("unlisted", "int")
    level_password = request_get("password", "int")
    original = request_get("original", "int")
    objects = request_get("objects", "int")
    song_id = request_get("songID", "int")
    coins = request_get("coins", "int")
    ldm = request_get("ldm", "int")

    # 2.2
    song_ids = request_get("songIDs")
    sfx_ids = request_get("sfxIDs")
    ts = request_get("ts", int)

    gd_version = check_version()

    if gd_version >= 22:
        friend_only = 1 if unlisted == 1 else 0
        unlisted = 1 if unlisted >= 1 else 0
    else:
        friend_only = 0

    if getsizeof(level_string) > MAXIMUM_LEVEL_SIZE:
        logger.info(f"Пользователь превысил лимит блоков ({account_id})")
        return "-1"

    if len(level_name) == 0 or len(level_string) == 0:
        logger.info(f"Некорректное имя уровня или levelstring "
                    f"({account_id}, name={len(level_name)}, level_string={len(level_string)})")
        return "-1"

    if not limit_check(
        (level_length, 5 if gd_version >= 22 else 4),
        (len(base64_decode(level_desc)), 180 if gd_version >= 22 else 140), (two_player, 1),
        (unlisted, 2 if gd_version >= 22 else 1), (len(str(original)), 12), (coins, 3), (ldm, 1), (len(level_name), 20)
    ):
        logger.info(f"Уровень не подходит под критерии защиты ({account_id})")
        logger.info("Подробная информация: " + "; ".join(
            [f"{i}={j}" for i, j in {
                "gd_version": gd_version,
                "level_name_len": len(level_name),
                "level_length": level_length,
                "level_desc_len": len(base64_decode(level_desc)),
                "two_player": two_player,
                "unlisted": unlisted,
                "original_id": len(str(original)),
                "coins": coins,
                "ldm": ldm,
            }.items()]
        ))
        return "-1"

    if limit_check((objects, MINIMUM_NUMBER_BLOCKS)) or objects <= 0:
        logger.info(f"Уровень не проходит по критерии минимального кол-во блоков "
                    f"({account_id}, {objects})")
        return "-1"

    if db.song.count_documents({
        "_id": song_id
    }) == 0 and song_id != 0:
        logger.info(f"Музыки под id {song_id} не существует ({account_id})")
        return "-1"

    is_official_song = 1 if song_id <= 0 else 0

    song_id = audio_track if bool(is_official_song) else song_id
    level_id = request_get("levelID", "int")

    username = db.account.find_one({"_id": account_id})["username"]

    if level_id == 0:
        logger.debug("Загрузка нового уровня на сервер")

        if not request_limiter(
            db.level, {"account_id": account_id}, limit_time=300
        ):
            logger.info(f"Пользователь не может выложить новый уровень, "
                        f"раньше чем через 5 минут ({account_id})")
            return "-1"

        level_id = last_id(db.level)
        level_id = level_id if level_id >= 100 else 100  # Зарезервировано от 1 до 100 идентификаторов уровней

        while level_id in RESERVED_LEVEL_IDS:
            level_id += 1

        with open(join(
            PATH_TO_ROOT, "data", "level", f"{str(level_id)}.level"
        ), "w") as file:
            file.write(level_string)

        sample_level = {
            "_id": level_id, "account_id": account_id, "username": db.account.find_one({"_id": account_id})["username"],
            "name": level_name, "desc": level_desc, "likes": 0, "downloads": 0, "version": 1, "length": level_length,
            "objects": objects, "password": level_password, "extra_string": extra_string,
            "coins": coins, "is_silver_coins": 0, "difficulty": 0, "stars": 0, "featured": 0, "epic": 0,
            "legendary": 0, "mythic": 0, "auto": 0, "demon": 0, "demon_type": 0, "song_id": song_id,
            "is_official_song": is_official_song, "original_id": original, "two_player": two_player,
            "unlisted": unlisted, "friend_only": friend_only, "ldm": ldm, "upload_time": int(time()), "update_time": 0,
            "rate_time": 0, "is_deleted": 0, "delete_prohibition": 0, "update_prohibition": 0, "song_ids": song_ids,
            "sfx_ids": sfx_ids, "game_version": gd_version, "ts": ts
        }

        db.level.insert_one(sample_level)

        plugin_manager.call_event("on_level_upload", level_id, level_name, account_id, username)
        logger.success(f"Пользователь удачно загрузил новый уровень ({account_id}, {level_id})!")

        return str(level_id)

    elif db.level.count_documents({
        "_id": level_id, "account_id": account_id,
        "update_prohibition": 0, "is_deleted": 0
    }) == 1:
        logger.debug(f"Обновление существующего уровня ({level_id})")

        if not request_limiter(
            db.level, {"_id": level_id, "account_id": account_id}, date="update_time", limit_time=300
        ):
            logger.info(f"Пользователь не может обновить уровень, "
                        f"раньше чем через 5 минут ({account_id})")
            return "-1"

        single_level = tuple(db.level.find({"_id": level_id}))
        level_version = single_level[0]["version"]

        with open(join(
            PATH_TO_ROOT, "data", "level", f"{str(level_id)}.level"
        ), "r") as file:
            old_level_string = file.read()

        with open(join(
            PATH_TO_ROOT, "data", "level", f"{str(level_id)}.level"
        ), "w") as file:
            file.write(level_string)

        with open(join(
            PATH_TO_ROOT, "data", "level", "old", f"{str(level_id)}v{level_version}.old.level"
        ), "w") as file:
            file.write(old_level_string)

        with open(join(
                PATH_TO_ROOT, "data", "level", "old", f"{str(level_id)}v{level_version}.old.level.db"
        ), "w") as file:
            file.write(json.dumps(single_level[0]))

        db.level.update_one({"_id": level_id}, {"$set": {
            "desc": level_desc,
            "version": level_version + 1,
            "password": level_password,
            "song_id": song_id,
            "is_official_song": is_official_song,
            "two_player": two_player,
            "objects": objects,
            "coins": coins,
            "extra_string": extra_string,
            "update_time": int(time()),
            "ldm": ldm,
            "song_ids": song_ids,
            "sfx_ids": sfx_ids,
            "game_version": gd_version,
            "ts": ts
        }})

        plugin_manager.call_event("on_level_update", level_id, level_version + 1, account_id, username)
        logger.success(f"Пользователь удачно обновил уровень ({account_id}, {level_id})!")

        return str(level_id)

    return "-1"
