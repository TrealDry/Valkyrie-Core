from config import MEMCACHE_LIFETIME
from bcrypt import hashpw, gensalt, checkpw
from utils import encoding, request_get, database as db, memcache as mc


def decoding_gjp(gjp):
    return encoding.xor(encoding.base64_decode(gjp), "37526")


def password_hashing(password):
    return hashpw(password.encode(), gensalt()).decode('ascii')


def check_password(account_id, password, ip=None,
                   is_gjp=True, is_check_valid=True, fast_mode=True):
    if fast_mode:
        ip = request_get.ip() if ip is None else ip

        if mc.client.get(f"CT:{account_id}:passwd") == ip.encode():
            return True

    if account_id <= 0 or account_id is None:
        return False

    if len(password) > 100:
        return False

    if db.account.count_documents(
        {"_id": account_id, "is_banned": 1}
    ) == 1:
        return False

    if is_check_valid:
        if db.account.count_documents({
            "_id": account_id, "is_valid": 0
        }) == 1:
            return False

    if is_gjp:
        password = decoding_gjp(password)

    try:
        if checkpw(
            password.encode(),
            db.account.find_one({"_id": account_id})["password"].encode()
        ):
            if is_check_valid and fast_mode:
                mc.client.set(f"CT:{account_id}:passwd", ip, MEMCACHE_LIFETIME)
            return True
        else:
            return False
    except TypeError:
        return False
