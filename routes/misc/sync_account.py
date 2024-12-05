from . import misc
from os.path import join
from loguru import logger
from config import PATH_TO_ROOT

from utils import database as db

from utils.regex import char_clean
from utils.passwd import check_password
from utils.check_secret import check_secret
from utils.plugin_manager import plugin_manager
from utils.request_get import request_get, get_ip


@misc.route("/database/accounts/syncGJAccountNew.php", methods=("POST", "GET"))
def sync_account():
    if not check_secret(
        request_get("secret"), 0
    ):
        logger.debug(f"Секретный ключ не совпал ({request_get("secret")})")
        return "-1"

    username = char_clean(request_get("userName"))
    password = request_get("password")

    account_id = request_get("accountID", "int")
    is_gjp2 = False

    ip = get_ip()

    if request_get("gjp2") != "":
        logger.debug(f"Используется gjp2 (версия игры >= 2.2)")

        is_gjp2 = True
        password = request_get("gjp2")

    if account_id <= 0:
        try:
            account_id = db.account_stat.find_one(
                {"username": {"$regex": f"^{username}$", '$options': 'i'}})["_id"]
        except:
            logger.info(f"Аккаунта не существует ({username}, {ip})")
            return "-1"

    if not check_password(
        account_id, password, fast_mode=False,
        is_gjp=False, is_gjp2=is_gjp2
    ):
        logger.info(f"Пароль не совпадает ({account_id}, {ip})!")
        return "-1"

    try:
        with open(join(
            PATH_TO_ROOT, "data", "account", f"{account_id}.account"
        ), "r") as file:
            save_data = file.read()
    except FileNotFoundError:
        logger.info(f"Бэкапа не существует ({account_id})!")
        return "-1"

    plugin_manager.call_event("on_player_sync", account_id, username)
    logger.success(f"Пользователь удачно синхронизировался ({account_id})!")

    return save_data + ";21;30;a;a"
