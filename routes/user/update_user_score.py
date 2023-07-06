from . import user
from config import PATH_TO_DATABASE
from utils import check_secret, limit_check, passwd, request_get as rg, database as db


"""
RU: Обязательно меняйте лимиты при росте приватного сервера!
EN: Be sure to change the limits as your private server grows!
"""

limits = {
    "stars": 5000,
    "demons": 500,
    "diamonds": 999999999,
    "user_coins": 1000,
    "secret_coins": 100
}


@user.route(f"{PATH_TO_DATABASE}/updateGJUserScore22.php", methods=("POST", "GET"))
def update_user_score():
    if not check_secret.main(
        rg.main("secret"), 1
    ):
        return "-1"

    account_id = rg.main("accountID", "int")
    password = rg.main("gjp")

    if not passwd.check_password(
        account_id, password
    ):
        return "-1"

    start = rg.main("stars", "int")
    demons = rg.main("demons", "int")
    diamonds = rg.main("diamonds", "int")
    user_coins = rg.main("userCoins", "int")
    secret_coins = rg.main("coins", "int")

    icon_type = rg.main("iconType", "int")  # 6
    icon_id = rg.main("icon", "int")  # 142
    icon_cube = rg.main("accIcon", "int")  # 142
    icon_ship = rg.main("accShip", "int")  # 51
    icon_ball = rg.main("accBall", "int")  # 43
    icon_ufo = rg.main("accBird", "int")  # 35
    icon_wave = rg.main("accDart", "int")  # 35
    icon_robot = rg.main("accRobot", "int")  # 26
    icon_spider = rg.main("accSpider", "int")  # 17
    icon_glow = rg.main("accGlow", "int")  # 1
    first_color = rg.main("color1", "int")  # 41
    second_color = rg.main("color2", "int")  # 41

    if not limit_check.main(
        (start, limits["stars"]), (demons, limits["demons"]), (diamonds, limits["diamonds"]),
        (user_coins, limits["user_coins"]), (secret_coins, limits["secret_coins"]), (icon_type, 6),
        (icon_id, 142), (icon_cube, 142), (icon_ship, 51), (icon_ball, 43), (icon_ufo, 35), (icon_wave, 35),
        (icon_robot, 26), (icon_spider, 17), (icon_glow, 1), (first_color, 41), (second_color, 41)
    ):
        return "-1"

    db.account_stat.update_one({"_id": account_id}, {"$set": {
        "stars": start,
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
        "icon_glow": icon_glow,
        "first_color": first_color,
        "second_color": second_color
    }})

    return str(account_id)
