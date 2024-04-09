from . import level
from config import PATH_TO_DATABASE

from utils.check_secret import check_secret
from utils.plugin_manager import plugin_manager
from utils.request_get import request_get, get_ip


@level.route(f"{PATH_TO_DATABASE}/reportGJLevel.php", methods=("POST", "GET"))
def report_stars():
    if not check_secret(
        request_get("secret"), 1
    ):
        return "-1"

    level_id = request_get("levelID")
    ip = get_ip()

    plugin_manager.call_event("on_level_report", level_id, ip)

    return "1"
