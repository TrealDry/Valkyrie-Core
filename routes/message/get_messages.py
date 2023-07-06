from . import message
from pymongo import DESCENDING
from config import PATH_TO_DATABASE
from utils import check_secret, passwd, request_get as rg, \
    database as db, time_converter as tc, response_processing as rp


@message.route(f"{PATH_TO_DATABASE}/getGJMessages20.php", methods=("POST", "GET"))
def get_messages():
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

    is_sender = rg.main("getSent", "int")

    query = {}
    response = ""

    query[
        "recipient_id" if is_sender == 0 else "account_id"
    ] = account_id

    messages = tuple(db.message.find(query).skip(offset).limit(10).sort([("_id", DESCENDING)]))

    for msg in messages:
        is_read = msg["is_read"] if is_sender == 0 else 1

        user_info = tuple(db.account_stat.find({
            "_id": msg["account_id"] if is_sender == 0 else msg["recipient_id"]
        }))

        prefix = user_info[0]["prefix"]
        prefix = prefix + " / " if prefix != "" else ""

        single_response = {
            6: user_info[0]["username"], 3: user_info[0]["_id"],
            2: user_info[0]["_id"], 1: msg["_id"], 4: msg["subject"],
            8: is_read, 9: is_sender, 7: prefix + tc.main(msg["upload_time"])
        }

        response += rp.main(single_response) + "|"

    response = response[:-1] + f"#{db.message.count_documents(query)}:{page * 50}:{page * 50 + 50}"

    return response
