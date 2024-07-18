from . import level
from config import PATH_TO_DATABASE

from utils.passwd import check_password
from utils.request_get import request_get
from utils.check_secret import check_secret
from utils.plugin_manager import plugin_manager


@level.route(f"{PATH_TO_DATABASE}/rateGJStars211.php", methods=("POST", "GET"))
def rate_stars():
    if not check_secret(
        request_get("secret"), 1
    ):
        return "-1"

    account_id = request_get("accountID", "int")
    password = request_get("gjp")

    is_gjp2 = False

    if request_get("gjp2") != "":
        is_gjp2 = True
        password = request_get("gjp2")

    if not check_password(
        account_id, password,
        is_gjp=not is_gjp2, is_gjp2=is_gjp2
    ):
        return "-1"

    stars = request_get("stars", "int")
    level_id = request_get("levelID", "int")

    plugin_manager.call_event("on_level_rate_stars", level_id, account_id, stars)

    return "1"  # Заглушка
