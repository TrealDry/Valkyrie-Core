from . import relationship
from config import PATH_TO_DATABASE
from utils import check_secret, passwd, \
    request_get as rg, database as db


@relationship.route(f"{PATH_TO_DATABASE}/blockGJUser20.php", methods=("POST", "GET"))
def block_user():
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

    target_id = rg.main("targetAccountID", "int")

    if account_id == target_id:
        return "1"

    if db.block_list.count_documents({"_id": account_id}) == 0:
        db.block_list.insert_one({
            "_id": account_id, "block_list": []
        })

    if db.block_list.count_documents({
        "_id": account_id, "block_list": {"$in": (target_id,)}
    }) == 1:
        return "1"

    if db.friend_list.count_documents({
        "_id": account_id, "friend_list": {"$in": (target_id,)}
    }) == 1:
        db.friend_list.update_one({"_id": account_id}, {"$pull": {"friend_list": target_id}})
        db.friend_list.update_one({"_id": target_id}, {"$pull": {"friend_list": account_id}})

    friend_req_query = {"$or": [
        {"account_id": account_id, "recipient_id": target_id},
        {"account_id": target_id, "recipient_id": account_id}
    ]}

    if db.friend_req.count_documents(friend_req_query) == 1:
        request = db.friend_req.find(friend_req_query)[0]

        db.account_stat.update_one({"_id": request["recipient_id"]}, {"$inc": {
            "friend_requests": -1
        }})

        db.friend_req.delete_one({"_id": request["_id"]})

    db.block_list.update_one({"_id": account_id}, {"$push": {"block_list": target_id}})

    return "1"
