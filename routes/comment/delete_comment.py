from . import comment
from config import PATH_TO_DATABASE
from utils import check_secret, passwd, \
    request_get as rg, database as db


@comment.route(f"{PATH_TO_DATABASE}/deleteGJComment20.php", methods=("POST", "GET"))
def delete_comment():
    if not check_secret.main(
        rg.main("secret"), 1
    ):
        return "-1"

    account_id = rg.main("accountID", "int")
    password = rg.main("gjp")

    level_id = rg.main("levelID", "int")
    comment_id = rg.main("commentID", "int")

    if not passwd.check_password(
        account_id, password
    ):
        return "-1"

    if db.level_comment.count_documents({
        "_id": comment_id, "level_id": level_id
    }) == 1:

        if db.level.count_documents({
            "_id": level_id, "account_id": account_id
        }) == 1:  # Если это твой уровень, то удалить комментарий можно
            pass

        elif db.level_comment.count_documents({
            "_id": comment_id, "account_id": account_id,
            "level_id": level_id
        }) == 0:  # Иначе, если это не твой комментарий, то пошёл куда подальше
            return "-1"

    else:
        return "-1"

    db.level_comment.delete_one({"_id": comment_id})
    return "1"
