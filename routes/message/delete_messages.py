from . import message
from config import PATH_TO_DATABASE
from utils import check_secret, passwd, request_get as rg, \
    database as db, time_converter as tc, response_processing as rp


@message.route(f"{PATH_TO_DATABASE}/deleteGJMessages20.php", methods=("POST", "GET"))
def delete_messages():
    if not check_secret.main(
        rg.main("secret"), 1
    ):
        return "1"

    account_id = rg.main("accountID", "int")
    password = rg.main("gjp")

    if not passwd.check_password(
        account_id, password
    ):
        return "1"

    message_id = rg.main("messageID", "int")
    message_ids = rg.main("messages")

    if message_ids != "":
        message_ids = message_ids.split(",")
    else:
        message_ids = None

    query = {"_id": message_id} if message_ids is None else \
            {"_id": {"$in": message_ids}}
    messages = tuple(db.message.find(query))

    for msg in messages:
        if msg["account_id"] != account_id and \
           msg["recipient_id"] != account_id:
            return "1"

        if msg["is_read"] == 0:
            db.account_stat.update_one(
                {"_id": msg["account_id"] if msg["recipient_id"] == account_id else msg["recipient_id"]},
                {"$inc": {
                    "missed_messages": -1
                }}
            )

        db.message.delete_one({"_id": msg["_id"]})

    return "1"
