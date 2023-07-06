from . import level
from config import PATH_TO_DATABASE
from utils import passwd, check_secret, request_get as rg, \
    database as db


@level.route(f"{PATH_TO_DATABASE}/rateGJDemon21.php", methods=("POST", "GET"))
def rate_demon():
    if not check_secret.main(
        rg.main("secret"), 3
    ):
        return "-1"

    account_id = rg.main("accountID", "int")
    password = rg.main("gjp")

    level_id = rg.main("levelID", "int")
    demon_type = rg.main("rating", "int")

    if not passwd.check_password(
        account_id, password
    ):
        return "-1"

    if db.role_assign.count_documents({
        "_id": account_id
    }) == 0:
        return "-1"

    if db.level.count_documents({
        "_id": level_id, "is_deleted": 0
    }) == 0:
        return "-1"

    if demon_type < 0 or demon_type > 5:
        return "-1"

    db.level.update_one({"_id": level_id}, {"$set": {
        "demon_type": demon_type
    }})

    return str(level_id)
