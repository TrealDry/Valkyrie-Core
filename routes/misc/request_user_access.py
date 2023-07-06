from . import misc
from config import PATH_TO_DATABASE
from utils import check_secret, passwd, \
    request_get as rg, database as db


@misc.route(f"{PATH_TO_DATABASE}/requestUserAccess.php", methods=("POST", "GET"))
def request_user_access():
    if not check_secret.main(
        rg.main("secret"), 1
    ):
        return "1"

    account_id = rg.main("accountID", "int")
    password = rg.main("gjp")

    if not passwd.check_password(
        account_id, password
    ):
        return "-1"

    if db.role_assign.count_documents({
        "_id": account_id
    }) == 0:
        return "-1"

    role_id = db.role_assign.find_one({"_id": account_id})["role_id"]
    role = db.role.find({"_id": role_id})

    badge = 2 if role[0]["mod_level"] > 1 else 1

    db.account_stat.update_one({"_id": account_id}, {"$set": {
        "mod_level": badge,
        "comment_color": role[0]["comment_color"]
    }})

    return str(badge)
