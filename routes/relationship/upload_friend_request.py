from time import time
from . import relationship
from config import PATH_TO_DATABASE
from utils import check_secret, passwd, last_id,\
    request_get as rg, database as db, encoding as enc


@relationship.route(f"{PATH_TO_DATABASE}/uploadFriendRequest20.php", methods=("POST", "GET"))
def upload_friend_request():
    if not check_secret.main(
        rg.main("secret"), 1
    ):
        return "-1"

    account_id = rg.main("accountID", "int")
    password = rg.main("gjp")

    recipient_id = rg.main("toAccountID", "int")
    comment = rg.main("comment")

    if not passwd.check_password(
        account_id, password
    ):
        return "-1"

    if len(enc.base64_decode(comment)) > 140:
        return "-1"

    if account_id == recipient_id:
        return "-1"

    if db.account_stat.count_documents(
        {"account_id": recipient_id, "friends_state": 1}
    ) == 1:
        return "-1"

    if db.friend_req.count_documents({"$or": [
        {"account_id": account_id, "recipient_id": recipient_id},
        {"account_id": recipient_id, "recipient_id": account_id}
    ]}) == 1:
        return "-1"

    if db.friend_list.count_documents({
        "_id": account_id, "friend_list": {"$in": [recipient_id]}
    }) == 1:
        return "-1"

    if db.block_list.count_documents({"$or": [
        {"_id": account_id, "block_list": {"$in": [recipient_id]}},
        {"_id": recipient_id, "block_list": {"$in": [account_id]}},
    ]}) == 1:
        return "-1"

    db.friend_req.insert_one({
        "_id": last_id.main(db.friend_req),
        "account_id": account_id,
        "recipient_id": recipient_id,
        "comment": comment,
        "timestamp": int(time())
    })

    db.account_stat.update_one({"_id": recipient_id}, {"$inc": {
        "friend_requests": 1
    }})

    return "1"
