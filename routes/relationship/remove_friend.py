from . import relationship
from config import PATH_TO_DATABASE
from utils import check_secret, passwd, request_get as rg, \
    database as db


@relationship.route(f"{PATH_TO_DATABASE}/removeGJFriend20.php", methods=("POST", "GET"))
def remove_friend():
    if not check_secret.main(
        rg.main("secret"), 1
    ):
        return "-1"

    account_id = rg.main("accountID", "int")
    password = rg.main("gjp")

    target_id = rg.main("targetAccountID", "int")

    if not passwd.check_password(
        account_id, password
    ):
        return "-1"

    if db.friend_list.count_documents({
        "_id": account_id, "friend_list": {"$in": (target_id,)}
    }) == 0:
        return "-1"

    db.friend_list.update_one({"_id": account_id}, {"$pull": {"friend_list": target_id}})
    db.friend_list.update_one({"_id": target_id}, {"$pull": {"friend_list": account_id}})

    return "1"
