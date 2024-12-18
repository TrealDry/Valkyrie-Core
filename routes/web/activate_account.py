from . import web
from loguru import logger
from flask import request, render_template
from config import (
    HCAPTCHA_SITE_KEY, ACCOUNTS_ACTIVATION_VIA_MAIL, REDIS_PREFIX
)

from utils import database as db

from utils.regex import char_clean
from utils.hcaptcha import hcaptcha
from utils.redis_db import client as rd
from utils.passwd import check_password
from utils.plugin_manager import plugin_manager
from utils.request_get import request_get, get_ip


@web.route("/activate_account", methods=("POST", "GET"))
def activate_account():
    message = ""
    code = ""
    account_id = 0

    ip = get_ip()

    try:
        if ACCOUNTS_ACTIVATION_VIA_MAIL:
            logger.debug("Верификация проходит при помощи почты")
            code = request_get("code")

            if code is None:
                logger.debug("Этого кода не существует (None)")
                return "Code is invalid!"

            account_id = rd.get(f"{REDIS_PREFIX}:{code}:confirm")

            if account_id is None:
                logger.debug(f"Заявки на верификацию ({account_id}) нет")
                return "Code is invalid!"

            account_id = int(account_id.decode())

        if request.method != "POST":
            raise

        if not ACCOUNTS_ACTIVATION_VIA_MAIL:
            logger.debug("Верификация проходит Без помощи почты")

            username = char_clean(request_get('login'))

            try:
                account_id = db.account.find_one(
                    {"username": {"$regex": f"^{username}$", '$options': 'i'}})["_id"]

            except IndexError:
                logger.debug(f"Такого имени ({username}) не существует")
                message = "Wrong login!"
                raise

            except Exception as e:
                logger.warning(f"Произошла неизвестная ошибка ({e})")
                raise

        password = request_get("password")

        if not hcaptcha.verify():
            message = "Captcha failed!"
            logger.debug("Капча была провалена")
            raise

        if db.account.count_documents({
            "_id": account_id, "is_valid": 1
        }) == 1:
            logger.debug("Аккаунт уже верифицирован")
            message = "Account already verified!"
            raise

        if not check_password(
            account_id, password,
            is_gjp=False, is_check_valid=False, fast_mode=False, is_gjp2=False
        ):
            logger.debug("Неправильный пароль")
            message = "Wrong password!"
            raise

        username = db.account.find_one({"_id": account_id})["username"]

        sample_account_stat = {
            "_id": account_id, "username": username, "stars": 0, "moons": 0, "demons": 0, "diamonds": 0,
            "user_coins": 0, "secret_coins": 0, "creator_points": 0, "first_color": 0, "second_color": 3,
            "third_color": -1, "icon_id": 1, "icon_type": 0, "icon_cube": 1, "icon_ship": 1, "icon_ball": 1,
            "icon_ufo": 1, "icon_wave": 1, "icon_robot": 1, "icon_spider": 1, "icon_glow": 0,
            "icon_swing_copter": 1, "icon_jetpack": 1, "missed_messages": 0, "friend_requests": 0,
            "message_state": 0, "friends_state": 0, "comment_history_state": 0, "youtube": "", "twitter": "",
            "twitch": "", "global_rank": 0, "is_banned": 0, "is_top_banned": 0, "prefix": "",
            "comment_color": "", "mod_badge": 0, "vip_status": 0, "small_chest_time": 0, "big_chest_time": 0,
            "small_chest_counter": 0, "big_chest_counter": 0, "level_statistics": {
                "daily_level": 0, "gauntlet_level": 0, "demon_ids": [], "weekly_demon": 0,
                "gauntlet_demon": 0, "auto_classic": 0, "easy_classic": 0, "normal_classic": 0,
                "hard_classic": 0, "harder_classic": 0, "insane_classic": 0, "auto_platformer": 0,
                "easy_platformer": 0, "normal_platformer": 0, "hard_platformer": 0,
                "harder_platformer": 0, "insane_platformer": 0
            }
        }

        db.account.update_one({"_id": account_id}, {"$set": {"is_valid": 1}})
        db.account_stat.insert_one(sample_account_stat)

        if ACCOUNTS_ACTIVATION_VIA_MAIL:
            logger.debug("Удаление записи заявки верификации")
            rd.delete(f"{REDIS_PREFIX}:{code}:confirm")

        plugin_manager.call_event("on_player_activate", account_id, username)
        logger.success(f"Верификация прошла успешно ({username}, {ip})!")


        return "Account verified!"
    except:
        html_file = "activate_account.html" if ACCOUNTS_ACTIVATION_VIA_MAIL else "activate_account_no_email.html"
        return render_template(html_file, SITE_KEY=HCAPTCHA_SITE_KEY, message=message)
