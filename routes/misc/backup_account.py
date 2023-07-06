from . import misc
from os.path import join
from sys import getsizeof
from config import PATH_TO_ROOT
from utils import passwd, regex, check_secret, request_get as rg, \
    database as db, memcache as mc


max_size = [15728640, 52428800]  # no vip, vip


@misc.route("/database/accounts/backupGJAccountNew.php", methods=("POST", "GET"))
def backup_account():
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

    if mc.client.get(f"CT:{account_id}:backup") == "1".encode():  # Проверка на тайм аут
        return "-1"

    save_data = rg.main("saveData")

    vip_status = db.account_stat.find_one({"_id": account_id})["vip_status"]

    if getsizeof(save_data) > max_size[vip_status]:
        return "-1"

    with open(join(
        PATH_TO_ROOT, "data", "account_backup", f"{account_id}.account"
    ), "w") as file:
        file.write(save_data)

    mc.client.set(f"CT:{account_id}:backup", "1", 60)  # Тайм аут 60 секунд

    return "1"
