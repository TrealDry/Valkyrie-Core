from . import score
from pymongo import DESCENDING
from config import PATH_TO_DATABASE, MEMCACHE_LIFETIME
from utils import check_secret, passwd, request_get as rg, \
    database as db, response_processing as rp, memcache as mc


def upload_scores(score_type="top"):  # for cron
    query = {"is_top_banned": 0}

    limit = 100
    sort = [("stars", DESCENDING)]

    if score_type == "top":
        query["stars"] = {"$gte": 10}
    elif score_type == "creators":
        query["creator_points"] = {"$gt": 0}
        sort = [("creator_points", DESCENDING)]

    response = ""

    users = db.account_stat.find(query).limit(limit)
    users.sort(sort)

    counter = 1

    for user in users:
        glow = 2 if user["icon_glow"] == 1 else 0

        single_response = {
            1: user["username"], 2: user["_id"], 13: user["secret_coins"], 17: user["user_coins"],
            6: counter, 9: user["icon_id"], 10: user["first_color"], 11: user["second_color"],
            14: user["icon_type"], 15: glow, 16: user["_id"], 3: user["stars"], 8: user["creator_points"],
            46: user["diamonds"], 4: user["demons"]
        }

        counter += 1
        response += rp.main(single_response) + "|"

    mc.client.set(f"CT:top:{score_type}", response, MEMCACHE_LIFETIME)

    return response


@score.route(f"{PATH_TO_DATABASE}/getGJScores20.php", methods=("POST", "GET"))
def get_scores():
    if not check_secret.main(
        rg.main("secret"), 1
    ):
        return "1"

    account_id = rg.main("accountID", "int")
    password = rg.main("gjp")

    score_type = rg.main("type")

    if not passwd.check_password(
        account_id, password
    ):
        return "1"

    if score_type == "" or score_type == "relative":
        score_type = "top"

    if score_type != "friends":
        cache = mc.client.get(f"CT:top:{score_type}")
        if cache is not None:
            return cache.decode()

    query = {"is_top_banned": 0}

    limit = 100
    sort = [("stars", DESCENDING)]

    if score_type == "top":

        query["stars"] = {"$gte": 10}

    elif score_type == "creators":

        query["creator_points"] = {"$gt": 0}
        sort = [("creator_points", DESCENDING)]

    elif score_type == "friends":

        return "1"

    else:

        return "-1"

    response = ""

    users = db.account_stat.find(query).limit(limit)
    users.sort(sort)

    counter = 1

    for user in users:
        glow = 2 if user["icon_glow"] == 1 else 0

        single_response = {
            1: user["username"], 2: user["_id"], 13: user["secret_coins"], 17: user["user_coins"],
            6: counter, 9: user["icon_id"], 10: user["first_color"], 11: user["second_color"],
            14: user["icon_type"], 15: glow, 16: user["_id"], 3: user["stars"], 8: user["creator_points"],
            46: user["diamonds"], 4: user["demons"]
        }

        counter += 1
        response += rp.main(single_response) + "|"

    if score_type != "friends":
        mc.client.set(f"CT:top:{score_type}", response, MEMCACHE_LIFETIME)

    return response
