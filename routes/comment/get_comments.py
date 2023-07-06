from . import comment
from pymongo import DESCENDING
from config import PATH_TO_DATABASE
from utils import check_secret, time_converter as tc, request_get as rg, \
    database as db, encoding as enc, response_processing as rp


@comment.route(f"{PATH_TO_DATABASE}/getGJComments21.php", methods=("POST", "GET"))
def get_comments():
    if not check_secret.main(
        rg.main("secret"), 1
    ):
        return "-1"

    level_id = rg.main("levelID", "int")

    page = rg.main("page", "int")
    offset = page * 10

    sort_mode = rg.main("mode", "int")
    sort = [("_id", DESCENDING)] if sort_mode == 0 else [("likes", DESCENDING)]

    query = {
        "level_id": level_id
    }

    comments = tuple(db.level_comment.find(query).skip(offset).limit(10).sort(sort))

    response = ""

    for i in comments:
        account_id = i["account_id"]
        user_info = tuple(db.account_stat.find({"_id": account_id}))

        prefix = user_info[0]["prefix"]
        prefix = prefix + " / " if prefix != "" else ""

        glow = user_info[0]["icon_glow"]
        glow = 2 if glow == 1 else glow

        single_comment_response = {
            2: enc.base64_decode(i["comment"]), 3: account_id, 4: i["likes"],
            7: 0, 10: i["percent"], 9: prefix + tc.main(i["upload_time"]),
            6: i["_id"], 11: user_info[0]["mod_level"]
        }

        if user_info[0]["comment_color"] != "":
            single_comment_response.update({12: user_info[0]["comment_color"]})

        response += rp.main(single_comment_response, 2)[:-1] + ":"

        single_user_response = {
            1: user_info[0]["username"], 9: user_info[0]["icon_id"], 10: user_info[0]["first_color"],
            11: user_info[0]["second_color"], 14: user_info[0]["icon_type"], 15: glow, 16: account_id
        }

        response += rp.main(single_user_response, 2) + "|"

    response = response + f"#{db.level_comment.count_documents(query)}:{offset}:10"

    return response
