from . import comment
from time import time
from config import PATH_TO_DATABASE
from utils import check_secret, request_limiter, commands, last_id, passwd, \
    request_get as rg, database as db, encoding as enc


@comment.route(f"{PATH_TO_DATABASE}/uploadGJComment21.php", methods=("POST", "GET"))
def upload_comment():
    if not check_secret.main(
        rg.main("secret"), 1
    ):
        return "-1"

    account_id = rg.main("accountID", "int")
    password = rg.main("gjp")

    level_comment = rg.main("comment")
    level_id = rg.main("levelID", "int")
    percent = rg.main("percent", "int")

    level_comment_decode = enc.base64_decode(level_comment)

    if not passwd.check_password(
        account_id, password
    ):
        return "-1"

    if not request_limiter.main(
        db.level_comment, {"account_id": account_id}, limit_time=15
    ):
        return "-1"

    if len(level_comment_decode) > 140 or len(level_comment_decode) == 0:
        return "-1"

    if percent > 100 or percent < 0:
        return "-1"

    if db.level.count_documents({
        "_id": level_id, "is_deleted": 0
    }) == 0:
        return "-1"

    if level_comment_decode[0] == "!":  # Команда
        commands.mod_commands(account_id, level_id, level_comment_decode)
        return "-1"

    sample_comment = {
        "_id": last_id.main(db.level_comment),
        "account_id": account_id,
        "level_id": level_id,
        "comment": enc.base64_encode(level_comment),
        "percent": percent,
        "likes": 0,
        "upload_time": int(time())
    }

    db.level_comment.insert_one(sample_comment)
    return "1"
