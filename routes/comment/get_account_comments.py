from . import comment
from pymongo import DESCENDING
from config import PATH_TO_DATABASE
from utils import check_secret, response_processing as rp, \
    time_converter as tc, request_get as rg, database as db


@comment.route(f"{PATH_TO_DATABASE}/getGJAccountComments20.php", methods=("POST", "GET"))
def get_account_comments():
    if not check_secret.main(
        rg.main("secret"), 1
    ):
        return "-1"

    account_id = rg.main("accountID", "int")

    prefix = db.account_stat.find_one({"_id": account_id})["prefix"]
    prefix = prefix + " / " if prefix != "" else ""

    page = rg.main("page", "int")

    offset = page * 10

    query = {
        "account_id": account_id
    }

    response = ""

    account_comments = tuple(db.account_comment.find(query).skip(offset).limit(10).sort([("_id", DESCENDING)]))

    for account_comment in account_comments:
        single_response = {
            2: account_comment["comment"], 4: account_comment["likes"],
            9: prefix + tc.main(account_comment["upload_time"]), 6: account_comment["_id"]
        }

        response += rp.main(single_response, 2) + "|"

    response = response[:-1] + f"#{db.account_comment.count_documents(query)}:{offset}:10"

    return response
