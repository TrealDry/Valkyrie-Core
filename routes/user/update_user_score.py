from . import user
from math import inf
from icecream import ic
from config import PATH_TO_DATABASE

from utils import database as db

from utils.endpoint_logging import logging
from utils.passwd import check_password
from utils.request_get import request_get
from utils.check_secret import check_secret
from utils.check_version import check_version
from utils.plugin_manager import plugin_manager
from utils.limit_check import limit_check, new_limit_check


"""
RUS: Обязательно меняйте лимиты при росте приватного сервера!
ENG: Be sure to change the limits as your private server grows!
"""

LIMIT = {
    "stars": 2500,
    "moons": 2500,
    "demons": 250,
    "diamonds": 999_999_999,
    "user_coins": 1000,
    "secret_coins": 100,

    "icons_21": {
        "icon_type": 6,
        "icon_id": 142,
        "icon_cube": 142,
        "icon_ship": 51,
        "icon_ball": 43,
        "icon_ufo": 35,
        "icon_wave": 35,
        "icon_robot": 26,
        "icon_spider": 17,
        "icon_swing_copter": 1,
        "icon_jetpack": 1,
        "icon_glow": 1,
        "first_color": 41,
        "second_color": 41,
        "third_color": 0
    },
    "icons_22": {
        "icon_type": 8,
        "icon_id": 484,
        "icon_cube": 484,
        "icon_ship": 169,
        "icon_ball": 118,
        "icon_ufo": 149,
        "icon_wave": 96,
        "icon_robot": 68,
        "icon_spider": 69,
        "icon_swing_copter": 43,
        "icon_jetpack": 5,
        "icon_glow": 1,
        "first_color": 107,
        "second_color": 107,
        "third_color": 107
    }
}


@user.route(f"{PATH_TO_DATABASE}/updateGJUserScore22.php", methods=("POST", "GET"))
def update_user_score():
    if not check_secret(
        request_get("secret"), 1
    ):
        return "-1"

    account_id = request_get("accountID", "int")
    password = request_get("gjp")

    gd_version = check_version()
    is_gjp2 = False

    if request_get("gjp2") != "":
        is_gjp2 = True
        password = request_get("gjp2")

    if not check_password(
        account_id, password, is_gjp=not is_gjp2, is_gjp2=is_gjp2
    ):
        return "-1"

    start = request_get("stars", "int")
    moons = 0
    demons = request_get("demons", "int")
    diamonds = request_get("diamonds", "int")
    user_coins = request_get("userCoins", "int")
    secret_coins = request_get("coins", "int")

    icon_type = request_get("iconType", "int")     # 6   : 8
    icon_id = request_get("icon", "int")           # 142 : 484
    icon_cube = request_get("accIcon", "int")      # 142 : 484
    icon_ship = request_get("accShip", "int")      # 51  : 169
    icon_ball = request_get("accBall", "int")      # 43  : 118
    icon_ufo = request_get("accBird", "int")       # 35  : 149
    icon_wave = request_get("accDart", "int")      # 35  : 96
    icon_robot = request_get("accRobot", "int")    # 26  : 68
    icon_spider = request_get("accSpider", "int")  # 17  : 69
    icon_swing_copter = 1
    icon_jetpack = 1
    icon_glow = request_get("accGlow", "int")      # 1   : 1
    first_color = request_get("color1", "int")     # 41  : 107
    second_color = request_get("color2", "int")    # 41  : 107
    third_color = 0

    demon_info = []
    demon_info_weekly = 0
    demon_info_gauntlet = 0

    level_info = [0] * 12
    level_info_daily = 0
    level_info_gauntlet = 0

    if gd_version == 22:
        moons = request_get("moons", "int")
        third_color = request_get("color3", "int")          # 107
        icon_swing_copter = request_get("accSwing", "int")  # 43
        icon_jetpack = request_get("accJetpack", "int")     # 5

        demon_info = request_get("dinfo", "list_int")
        demon_info_weekly = request_get("dinfow", "int")
        demon_info_gauntlet = request_get("dinfog", "int")

        level_info = request_get("sinfo", "list_int")
        level_info_daily = request_get("sinfod", "int")
        level_info_gauntlet = request_get("sinfog", "int")

    # == Проверка лимитов ==

    i_ver = f"icons_{gd_version}"

    if not limit_check(  # Игровая статистика
        (start, LIMIT["stars"]), (moons, LIMIT["moons"]), (demons, LIMIT["demons"]),
        (diamonds, LIMIT["diamonds"]), (user_coins, LIMIT["user_coins"]), (secret_coins, LIMIT["secret_coins"])
    ):
        return "-1"

    if not new_limit_check(  # Иконки и цвета
        (0, icon_type, LIMIT[i_ver]["icon_type"]),
        (1, icon_id, LIMIT[i_ver]["icon_id"]), (1, icon_cube, LIMIT[i_ver]["icon_cube"]),
        (1, icon_ship, LIMIT[i_ver]["icon_ship"]), (1, icon_ball, LIMIT[i_ver]["icon_ball"]),
        (1, icon_ufo, LIMIT[i_ver]["icon_ufo"]), (1, icon_wave, LIMIT[i_ver]["icon_wave"]),
        (1, icon_robot, LIMIT[i_ver]["icon_robot"]), (1, icon_spider, LIMIT[i_ver]["icon_spider"]),
        (1, icon_swing_copter, LIMIT[i_ver]["icon_swing_copter"]), (1, icon_jetpack, LIMIT[i_ver]["icon_jetpack"]),
        (0, icon_glow, LIMIT[i_ver]["icon_glow"]), (0, first_color, LIMIT[i_ver]["first_color"]),
        (0, second_color, LIMIT[i_ver]["second_color"]), (-1, third_color, LIMIT[i_ver]["third_color"])
    ):
        return "-1"

    if not limit_check(  # TODO Заменить INF заглушку
        (demon_info_weekly, inf), (demon_info_gauntlet, inf),
            (level_info_daily, inf), (level_info_gauntlet, inf),
            *list(zip(
                level_info + demon_info, [
                    inf for _ in range(len(level_info) + len(demon_info))
                ]
            ))
    ):
        return "-1"

    # == Никогда не доверяй вводу пользователей ==

    stats_before_update = tuple(db.account_stat.find({"_id": account_id}))[0]

    db.account_stat.update_one({"_id": account_id}, {"$set": {
        "stars": start,
        "moons": moons,
        "demons": demons,
        "diamonds": diamonds,
        "user_coins": user_coins,
        "secret_coins": secret_coins,
        "icon_id": icon_id,
        "icon_type": icon_type,
        "icon_cube": icon_cube,
        "icon_ship": icon_ship,
        "icon_ball": icon_ball,
        "icon_ufo": icon_ufo,
        "icon_wave": icon_wave,
        "icon_robot": icon_robot,
        "icon_spider": icon_spider,
        "icon_swing_copter": icon_swing_copter,
        "icon_jetpack": icon_jetpack,
        "icon_glow": icon_glow,
        "first_color": first_color,
        "second_color": second_color,
        "third_color": third_color,
        "level_statistics": {
            "daily_level": level_info_daily,
            "gauntlet_level": level_info_gauntlet,
            "demon_ids": demon_info,
            "weekly_demon": demon_info_weekly,
            "gauntlet_demon": demon_info_weekly,
            "auto_classic": level_info[0],
            "easy_classic": level_info[1],
            "normal_classic": level_info[2],
            "hard_classic": level_info[3],
            "harder_classic": level_info[4],
            "insane_classic": level_info[5],
            "auto_platformer": level_info[6],
            "easy_platformer": level_info[7],
            "normal_platformer": level_info[8],
            "hard_platformer": level_info[9],
            "harder_platformer": level_info[10],
            "insane_platformer": level_info[11]
        }
    }})

    plugin_manager.call_event(
        "on_player_score_update", account_id,
        {
            "stars": stats_before_update["stars"],
            "moons": stats_before_update["moons"],
            "demons": stats_before_update["demons"],
            "diamonds": stats_before_update["diamonds"],
            "user_coins": stats_before_update["user_coins"],
            "secret_coins": stats_before_update["secret_coins"]
        },
        {
            "stars": start,
            "moons": moons,
            "demons": demons,
            "diamonds": diamonds,
            "user_coins": user_coins,
            "secret_coins": secret_coins
        }
    )

    logging("debug")
    return str(account_id)
