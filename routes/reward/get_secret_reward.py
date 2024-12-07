from . import reward
from config import PATH_TO_DATABASE

from utils import database as db

from utils.xor import xor
from utils.passwd import check_password
from utils.chk_decoder import chk_decoder
from utils.request_get import request_get
from utils.check_secret import check_secret
from utils.base64_dec_and_enc import base64_decode, base64_encode

@reward.route(f"{PATH_TO_DATABASE}/getGJSecretReward.php", methods=("POST", "GET"))
def get_secret_reward():
    if not check_secret(
        request_get("secret"), 1
    ):
        return "-1"

    account_id = request_get("accountID", "int")
    password = request_get("gjp2")

    if not check_password(
        account_id, password,
        is_gjp=False, is_gjp2=True
    ):
        return "-1"

    chk = chk_decoder(request_get("chk"))
    vault_code = request_get("rewardKey")

    if 1 > len(vault_code) > 100:
        return "-1"
