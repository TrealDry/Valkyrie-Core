from . import account
from loguru import logger
from config import PATH_TO_DATABASE, REDIS_PREFIX

from utils import database as db

from utils.regex import char_clean
from utils.passwd import check_password
from utils.redis_db import client as rd
from utils.check_secret import check_secret
from utils.plugin_manager import plugin_manager
from utils.request_get import request_get, get_ip


LOGIN_ATTEMPTS_TIMELINE = 3600


@account.route(f"{PATH_TO_DATABASE}/accounts/loginGJAccount.php", methods=("POST", "GET"))
def login_account():
    ip = get_ip()
    login_attempts = rd.get(f"{REDIS_PREFIX}:{ip}:login")

    if login_attempts is not None:
        login_attempts = int(login_attempts)
        if login_attempts >= 8:
            logger.info(f"Пользователь ({ip}) превысил лимит попыток входа в аккаунт")
            return "-12"

    if not check_secret(
        request_get("secret"), 0
    ):
        logger.debug(f"Секретный ключ не совпал ({request_get("secret")})")
        return "-1"

    username = char_clean(request_get("userName"))
    password = request_get("password")

    is_gjp2 = False

    if 3 > len(username) > 15:
        logger.debug(f"Имя превысило лимиты ({len(username)} символов)")
        return "-11"

    # == Проверка длин паролей у разных версий (2.1 - 2.2) ==
    if request_get("gjp2") != "":  # >= 2.2
        password = request_get("gjp2")
        is_gjp2 = True

        if len(password) != 40:
            logger.debug(f"Пароль gjp2 не подходит под длину ({len(password)})")
            return "-1"

    else:  # <= 2.1
        if len(password) > 20:
            logger.debug(f"Обычный пароль не подходит под длину ({len(password)})")
            return "-11"
    # == ==

    fail_login = False

    try:
        account_id = db.account.find_one(
            {"username": {"$regex": f"^{username}$", '$options': 'i'}})["_id"]

        if not check_password(
            account_id, password, is_gjp=not is_gjp2,
            fast_mode=False, is_gjp2=is_gjp2
        ):
            raise
    except KeyError:
        logger.info(f"Аккаунта не существует ({username})!")
        fail_login = True
    except:
        logger.info(f"Вход не удался ({username}, {ip})!")
        fail_login = True

    if fail_login:
        if login_attempts is None:
            rd.set(f"{REDIS_PREFIX}:{ip}:login", 0, LOGIN_ATTEMPTS_TIMELINE)
            logger.debug("Новая попытка входа была записана")

        rd.incr(f"{REDIS_PREFIX}:{ip}:login", 1)
        logger.debug("+1 к попыткам входа")
        return "-11"

    plugin_manager.call_event("on_player_login", account_id, username)
    logger.success(f"Вход прошёл успешно ({username})!")

    return f"{account_id},{account_id}"
