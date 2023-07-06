from . import relationship
from pymongo import ASCENDING
from config import PATH_TO_DATABASE
from utils import check_secret, passwd, request_get as rg, \
    database as db, response_processing as rp


@relationship.route(f"{PATH_TO_DATABASE}/getGJUserList20.php", methods=("POST", "GET"))
def get_user_list():
    if not check_secret.main(
        rg.main("secret"), 1
    ):
        return "-1"

    account_id = rg.main("accountID", "int")
    password = rg.main("gjp")
    
    list_type = rg.main("type", "int")

    if not passwd.check_password(
        account_id, password
    ):
        return "-1"

    query = {
        "_id": account_id
    }

    user_ids = tuple(db.friend_list.find(query)) \
        if list_type == 0 else tuple(db.block_list.find(query))

    list_str = "friend_list" if list_type == 0 else "block_list"

    if not bool(user_ids) or not bool(user_ids[0][list_str]):
        return "-2"

    users = tuple(db.account_stat.find({"_id": {"$in": user_ids[0][list_str]}}).sort([("username", ASCENDING)]))
    response = ""

    for user in users:
        glow = 2 if user["icon_glow"] == 1 else 0

        single_response = {
            1: user["username"], 2: user["_id"], 9: user["icon_id"],
            10: user["first_color"], 11: user["second_color"], 14: user["icon_type"],
            15: glow, 16: user["_id"], 18: user["message_state"], 41: ""
        }

        response += rp.main(single_response) + "|"

    response = response[:-1]

    return response
