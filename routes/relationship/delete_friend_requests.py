from . import relationship
from config import PATH_TO_DATABASE
from utils import check_secret, passwd, request_get as rg, \
    database as db


@relationship.route(f"{PATH_TO_DATABASE}/deleteGJFriendRequests20.php", methods=("POST", "GET"))
def delete_friend_requests():
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

    target_id = rg.main("targetAccountID", "int")
    is_sender = rg.main("isSender", "int")

    query = {"account_id": target_id, "recipient_id": account_id} \
        if is_sender == 0 else {"account_id": account_id, "recipient_id": target_id}

    if db.friend_req.count_documents(query) == 0:
        return "1"

    db.friend_req.delete_one(query)
    db.account_stat.update_one({"_id": query["recipient_id"]}, {"$inc": {
        "friend_requests": -1
    }})

    return "1"
