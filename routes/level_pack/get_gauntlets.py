from . import level_pack
from config import PATH_TO_DATABASE
from utils import check_secret, request_get as rg, \
    database as db, level_hashing as lh, response_processing as rp


@level_pack.route(f"{PATH_TO_DATABASE}/getGJGauntlets21.php", methods=("POST", "GET"))
def get_gauntlets():
    if not check_secret.main(
        rg.main("secret"), 1
    ):
        return "1"

    gauntlets = tuple(db.gauntlet.find())

    response = ""
    hash_string = ""

    for gn in gauntlets:
        single_response = {
            1: gn["_id"], 3: gn["levels"]
        }

        hash_string += f"{gn['_id']}{gn['levels']}"
        response += rp.main(single_response) + "|"

    response = response[:-1] + f"#{lh.return_hash(hash_string)}"

    return response
