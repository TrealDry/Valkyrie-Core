from . import level
from config import PATH_TO_DATABASE
from utils import passwd, check_secret, request_get as rg, \
    database as db, encoding as enc


@level.route(f"{PATH_TO_DATABASE}/updateGJDesc20.php", methods=("POST", "GET"))
def update_desc():
    if not check_secret.main(
        rg.main("secret"), 1
    ):
        return "-1"

    account_id = rg.main("accountID", "int")
    password = rg.main("gjp")

    level_id = rg.main("levelID", "int")
    level_desc = rg.main("levelDesc")

    if not passwd.check_password(
        account_id, password
    ):
        return "-1"

    if db.level.count_documents({
        "_id": level_id, "account_id": account_id,
        "is_deleted": 0, "update_prohibition": 0
    }) == 0:
        return "-1"

    if len(enc.base64_decode(level_desc)) > 140:
        return "-1"

    db.level.update_one({"_id": level_id}, {"$set": {
        "desc": level_desc
    }})

    return "1"
