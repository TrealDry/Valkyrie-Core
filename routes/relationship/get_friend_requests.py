from . import relationship
from pymongo import DESCENDING
from config import PATH_TO_DATABASE
from utils import check_secret, passwd, request_get as rg, \
    database as db, time_converter as tc, response_processing as rp


@relationship.route(f"{PATH_TO_DATABASE}/getGJFriendRequests20.php", methods=("POST", "GET"))
def get_friend_requests():
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

    page = rg.main("page", "int")
    offset = page * 10

    type_request = rg.main("getSent", "int")

    query = {}
    response = ""

    query[
        "recipient_id" if type_request == 0 else "account_id"
    ] = account_id

    friend_reqs = tuple(db.friend_req.find(query).skip(offset).limit(10).sort([("_id", DESCENDING)]))

    for req in friend_reqs:
        user_info = tuple(db.account_stat.find({
            "_id": req["account_id"] if type_request == 0 else req["recipient_id"]
        }))

        glow = 2 if user_info[0]["icon_glow"] == 1 else 0

        single_response = {
            1: user_info[0]["username"], 2: user_info[0]["_id"], 9: user_info[0]["icon_id"],
            10: user_info[0]["first_color"], 11: user_info[0]["second_color"], 14: user_info[0]["icon_type"],
            15: glow, 16: user_info[0]["_id"], 32: req["_id"], 35: req["comment"], 41: 1,
            37: tc.main(req["timestamp"])
        }

        response += rp.main(single_response) + "|"

    response = response[:-1] + f"#:{page * 20}:20"

    return response
