from . import comment
from config import PATH_TO_DATABASE
from utils import check_secret, passwd, \
    request_get as rg, database as db


@comment.route(f"{PATH_TO_DATABASE}/deleteGJAccComment20.php", methods=("POST", "GET"))
def delete_account_comments():
    if not check_secret.main(
        rg.main("secret"), 1
    ):
        return "-1"

    account_id = rg.main("accountID", "int")
    password = rg.main("gjp")

    comment_id = rg.main("commentID", "int")

    if not passwd.check_password(
        account_id, password
    ):
        return "-1"

    if db.account_comment.count_documents({
        "_id": comment_id, "account_id": account_id
    }) == 0:
        return "-1"

    db.account_comment.delete_one({"_id": comment_id})

    return "1"
