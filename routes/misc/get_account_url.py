from . import misc
from config import PATH_TO_DATABASE, DOMAIN


@misc.route(f"{PATH_TO_DATABASE}/getAccountURL.php", methods=("POST", "GET"))
def get_account_uri():
    return DOMAIN
