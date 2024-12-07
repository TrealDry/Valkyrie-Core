from . import level
from time import time
from pymongo import DESCENDING
from config import PATH_TO_DATABASE

from utils import database as db

from utils.xor import xor
from utils.chk_decoder import chk_decoder
from utils.request_get import request_get
from utils.check_secret import check_secret
from utils.level_hashing import return_hash4
from utils.check_version import check_version
from utils.base64_dec_and_enc import base64_encode


@level.route(f"{PATH_TO_DATABASE}/getGJDailyLevel.php", methods=("POST", "GET"))
def get_daily_level():
    if not check_secret(
        request_get("secret"), 1
    ):
        return "-1"

    time_now = int(time())
    type_daily = 0

    if check_version() <= 21:
        type_daily = request_get("weekly", "int")
    elif check_version() >= 22:
        type_daily = request_get("type", "int")

    match type_daily:
        case 0: additional_id = 0       # daily
        case 1: additional_id = 100001  # weekly
        case 2: additional_id = 200001  # event
        case _: return "-1"

    time_limit = 604800 if type_daily == 1 else 86400

    try:
        daily_level = tuple(db.daily_level.find({
            "timestamp": {"$lte": time_now},
            "type_daily": type_daily
        }).sort([("timestamp", DESCENDING)]).limit(1))[0]
    except IndexError:
        return "-1"

    time_left = (daily_level['timestamp'] + time_limit) - time_now

    if time_left <= -1:
        return "-1"

    hash_result = ""

    if type_daily == 2:  # event
        chk = chk_decoder(request_get("chk"))

        first_hash = base64_encode(xor(
            f"vcore:{chk}:{daily_level["daily_id"] + 19}:"
            f"{daily_level["chest_type"]}:{daily_level["rewards"]}",
            "59182"
        ))
        second_hash = return_hash4(first_hash)
        hash_result = f"|vcore{first_hash}|{second_hash}"

        time_left = 10

    return f"{daily_level['daily_id'] + additional_id}|{time_left}{hash_result}"
