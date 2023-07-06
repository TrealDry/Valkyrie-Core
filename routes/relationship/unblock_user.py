from . import relationship
from config import PATH_TO_DATABASE
from utils import check_secret, passwd, \
    request_get as rg, database as db


@relationship.route(f"{PATH_TO_DATABASE}/unblockGJUser20.php", methods=("POST", "GET"))
def unblock_user():
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

    if db.block_list.count_documents({
        "_id": account_id, "block_list": {"$in": (target_id,)}
    }) == 1:
        db.block_list.update_one({"_id": account_id}, {"$pull": {"block_list": target_id}})

    return "1"
