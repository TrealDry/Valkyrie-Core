from . import misc
from os.path import join
from config import PATH_TO_ROOT
from utils import passwd, regex, check_secret, \
    request_get as rg, database as db


@misc.route("/database/accounts/syncGJAccountNew.php", methods=("POST", "GET"))
def sync_account():
    if not check_secret.main(
        rg.main("secret"), 0
    ):
        return "-1"

    username = regex.char_clean(rg.main("userName"))
    password = rg.main("password")

    try:
        account_id = db.account_stat.find_one(
            {"username": {"$regex": f"^{username}$", '$options': 'i'}})["_id"]
    except TypeError:
        return "-1"
    except KeyError:
        return "-1"

    if not passwd.check_password(
        account_id, password, is_gjp=False, fast_mode=False
    ):
        return "-1"

    try:
        with open(join(
            PATH_TO_ROOT, "data", "account_backup", f"{account_id}.account"
        ), "r") as file:
            save_data = file.read()
    except FileNotFoundError:
        return "-1"

    return save_data + ";21;30;a;a"
