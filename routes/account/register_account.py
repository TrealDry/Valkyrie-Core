import uuid
from time import time
from . import account
from loguru import logger
from threading import Thread

from config import (
    PATH_TO_DATABASE, ACCOUNTS_ACTIVATION_VIA_MAIL,
    GD_SERVER_NAME, DOMAIN, REDIS_PREFIX
)

from utils import database as db

from utils.last_id import last_id
from utils.regex import char_clean
from utils.redis_db import client as rd
from utils.mail_sender import mail_sender
from utils.check_secret import check_secret
from utils.plugin_manager import plugin_manager
from utils.request_get import request_get, get_ip
from utils.passwd import password_hashing, generate_gjp2


WHITELIST = True
WHITELIST_EMAILS = ["gmail.com", "ya.ru", "yandex.by", "yandex.com",
                    "yandex.kz", "yandex.ru", "mail.ru", "internet.ru",
                    "bk.ru", "inbox.ru", "list.ru"]


@account.route(f"{PATH_TO_DATABASE}/accounts/registerGJAccount.php", methods=("POST", "GET"))
def register_account():
    if not check_secret(
        request_get("secret"), 0
    ):
        logger.debug(f"Секретный ключ не совпал ({request_get("secret")})")
        return "-1"

    username = char_clean(request_get("userName"))
    password = request_get("password")
    email = request_get("email")

    ip = get_ip()

    # == Проверка лимита длины ==
    if len(username) < 3 or len(username) > 15:
        logger.debug(f"Имя превысило лимиты ({len(username)})")
        return "-4"

    if len(password) < 6 or len(password) > 20:
        logger.debug(f"Пароль превысил лимиты ({len(password)})")
        return "-5"

    if len(email) < 5 or len(email) > 32:
        logger.debug(f"Почтовый ящик превысил лимиты ({len(email)})")
        return "-6"
    # == ==

    if WHITELIST:
        if email.split("@")[1].lower() not in WHITELIST_EMAILS:
            logger.info(f"Почтовый ящик не прошёл белый список "
                        f"({email}, {ip})")
            return "-6"

    # == Существуют ли такое имя или электронная почта в базе данных ==
    if db.account.count_documents(
        {"username": {"$regex": f"^{username}$", '$options': 'i'}}
    ) == 1:
        logger.info(f"Имя уже занято ({username})")
        return "-2"

    if db.account.count_documents(
        {"email": {"$regex": f"^{email}$", '$options': 'i'}}
    ) == 1:
        logger.info(f"Почта уже занята ({email})")
        return "-3"
    # == ==

    account_id = last_id(db.account)

    if ACCOUNTS_ACTIVATION_VIA_MAIL:
        logger.debug("Верификация осуществляется при помощи почты")
        code = str(uuid.uuid4())

        message_data = {
            "title": f"Activate your account | {GD_SERVER_NAME}",
            "recipient": email,
            "body": f"Your username: {username}\nAccount activation link: {DOMAIN}/activate_account?code={code}"
        }

        sending_message = Thread(target=mail_sender, args=(message_data,))
        sending_message.start()

        rd.set(f"{REDIS_PREFIX}:{code}:confirm", account_id, 3600)
        logger.debug(f"Была создана заявка на верификацию (длительность 3600 секунд)")

    db.account.insert_one({
        "_id": account_id,
        "username": username,
        "password": password_hashing(password),
        "gjp2": generate_gjp2(password, bcrypt=True),
        "email": email,
        "date": int(time()),
        "is_banned": 0,
        "is_valid": 0
    })

    plugin_manager.call_event("on_player_new", account_id, username)
    logger.success(f"Аккаунт был зарегистрирован ({username}, {ip})!")

    return "1"
