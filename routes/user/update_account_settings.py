from . import user
from config import PATH_TO_DATABASE
from utils import passwd, check_secret, limit_check, \
    request_get as rg, database as db


@user.route(f"{PATH_TO_DATABASE}/updateGJAccSettings20.php", methods=("POST", "GET"))
def update_account_settings():
    if not check_secret.main(
        rg.main("secret"), 0
    ):
        return "-1"

    account_id = rg.main("accountID", "int")
    password = rg.main("gjp")

    if not passwd.check_password(
        account_id, password
    ):
        return "-1"

    message_status = rg.main("mS", "int")
    friend_status = rg.main("frS", "int")
    comment_status = rg.main("cS", "int")

    youtube_link = rg.main("yt")
    twitter_link = rg.main("twitter")
    twitch_link = rg.main("twitch")

    if not limit_check.main(
        (message_status, 2), (friend_status, 1), (comment_status, 2),
        (len(youtube_link), 30), (len(twitter_link), 20), (len(twitch_link), 30)
    ):
        return "-1"

    db.account_stat.update_one({"_id": account_id}, {"$set": {
        "message_state": message_status,
        "friends_state": friend_status,
        "comment_history_state": comment_status,
        "youtube": youtube_link,
        "twitter": twitter_link,
        "twitch": twitch_link
    }})

    return "1"
