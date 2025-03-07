from . import comment
from time import time
from config import PATH_TO_DATABASE, COMMAND_PREFIX

from utils import database as db

from utils.last_id import last_id
from utils.commands import commands
from utils.passwd import check_password
from utils.request_get import request_get
from utils.check_secret import check_secret
from utils.request_limiter import request_limiter
from utils.base64_dec_and_enc import base64_decode, base64_encode


@comment.route(f"{PATH_TO_DATABASE}/uploadGJComment21.php", methods=("POST", "GET"))
def upload_comment():
    if not check_secret(
        request_get("secret"), 1
    ):
        return "-1"

    account_id = request_get("accountID", "int")
    password = request_get("gjp")

    is_gjp2 = False

    if request_get("gjp2") != "":
        is_gjp2 = True
        password = request_get("gjp2")

    if not check_password(
        account_id, password,
        is_gjp=not is_gjp2, is_gjp2=is_gjp2
    ):
        return "-1"

    level_comment = request_get("comment")

    level_id = request_get("levelID", "int")
    is_level = 1 if level_id > 0 else 0

    percent = request_get("percent", "int")

    level_comment_decode = base64_decode(level_comment)

    if not request_limiter(
        db.level_comment, {"account_id": account_id}, limit_time=15
    ):
        return "-1"

    if len(level_comment_decode) > 140 or len(level_comment_decode) == 0:
        return "-1"

    if percent > 100 or percent < 0:
        return "-1"

    if is_level:
        if db.level.count_documents({
            "_id": level_id, "is_deleted": 0
        }) == 0:
            return "-1"
    elif not is_level:
        level_id *= -1

        if db.level_list.count_documents({
            "_id": level_id, "is_deleted": 0
        }) == 0:
            return "-1"

    if level_comment_decode[0] == COMMAND_PREFIX and is_level:  # Команда
        commands(account_id, level_id, level_comment_decode, is_level)
        return "-1"

    sample_comment = {
        "_id": last_id(db.level_comment),
        "account_id": account_id,
        "level_id": level_id,
        "is_level": is_level,
        "comment": base64_encode(level_comment),
        "percent": percent if is_level else 0,
        "likes": 0,
        "is_deleted": 0,
        "upload_time": int(time())
    }

    db.level_comment.insert_one(sample_comment)
    return "1"
