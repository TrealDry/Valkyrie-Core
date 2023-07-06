from . import account
from config import PATH_TO_DATABASE
from utils import check_secret, regex, passwd, \
    request_get as rg, database as db, memcache as mc


@account.route(f"{PATH_TO_DATABASE}/accounts/loginGJAccount.php", methods=("POST", "GET"))
def login_account():
    ip = rg.ip()
    login_attempts = mc.client.get(f"CT:{ip}:login")

    if login_attempts is not None:
        login_attempts = int(login_attempts.decode())
        if login_attempts >= 8:
            return "-12"

    if not check_secret.main(
        rg.main("secret"), 0
    ):
        return "-1"

    username = regex.char_clean(rg.main("userName"))
    password = rg.main("password")

    if len(username) > 15 or len(password) > 20:
        return "-1"

    try:
        account_id = db.account.find_one(
            {"username": {"$regex": f"^{username}$", '$options': 'i'}})["_id"]

        if not passwd.check_password(
            account_id, password, is_gjp=False, fast_mode=False
        ):
            raise
    except:
        if login_attempts is None:
            mc.client.set(f"CT:{ip}:login", 0, 3600)

        mc.client.incr(f"CT:{ip}:login", 1)
        return "-1"

    return f"{account_id},{account_id}"
