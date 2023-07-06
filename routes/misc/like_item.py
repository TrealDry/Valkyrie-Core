from . import misc
from utils import check_secret, passwd, \
    request_get as rg, database as db
from config import PATH_TO_DATABASE, PROTECTION_AGAINST_DISLIKE_BOTS


@misc.route(f"{PATH_TO_DATABASE}/likeGJItem211.php", methods=("POST", "GET"))
def like_item():
    if not check_secret.main(
        rg.main("secret"), 1
    ):
        return "1"

    account_id = rg.main("accountID", "int")
    password = rg.main("gjp")

    item_id = rg.main("itemID", "int")
    item_type = rg.main("type", "int")

    like = 1 if rg.main("like", "int") != 0 else -1

    if not passwd.check_password(
        account_id, password
    ):
        return "1"

    if db.action_like.count_documents({
        "item_id": item_id,
        "item_type": item_type,
        "account_id": account_id
    }) == 1:
        return "1"

    if item_type == 1:  # Уровень
        coll = db.level
    elif item_type == 2:  # Комментарий к уровню
        coll = db.level_comment
    elif item_type == 3:  # Комментарий на аккаунте
        coll = db.account_comment
    else:
        return "1"

    if coll.count_documents({
        "_id": item_id
    }) == 0:
        return "1"

    if item_type == 1 and coll.count_documents({
        "_id": item_id, "is_deleted": 0
    }) == 0:
        return "1"
    elif PROTECTION_AGAINST_DISLIKE_BOTS:
        if db.action_download.count_documents({
            "level_id": item_id, "account_id": account_id
        }) == 0:
            return "1"

    coll.update_one({"_id": item_id}, {"$inc": {"likes": like}})

    sample_action_like = {
        "item_id": item_id,
        "item_type": item_type,
        "account_id": account_id,
    }

    db.action_like.insert_one(sample_action_like)

    return "1"
