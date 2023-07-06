import os
from . import level
from os.path import join
from threading import Thread
from config import PATH_TO_DATABASE, PATH_TO_ROOT
from utils import passwd, check_secret, request_get as rg, database as db


def removal_of_residues(level_id):
    level_id = str(level_id)

    all_files = os.listdir(
        join(PATH_TO_ROOT, "data", "old_level")
    )

    for file in all_files:
        if file[:len(level_id)] == level_id:
            os.remove(
                join(PATH_TO_ROOT, "data", "old_level", file)
            )

    return None


@level.route(f"{PATH_TO_DATABASE}/deleteGJLevelUser20.php", methods=("POST", "GET"))
def delete_level():
    if not check_secret.main(
        rg.main("secret"), 2
    ):
        return "-1"

    account_id = rg.main("accountID", "int")
    password = rg.main("gjp")

    level_id = rg.main("levelID", "int")

    if not passwd.check_password(
        account_id, password
    ):
        return "-1"

    if db.level.count_documents({
        "_id": level_id, "delete_prohibition": 0,
        "is_deleted": 0, "stars": 0, "account_id": account_id
    }) == 0:
        return "-1"

    db.level.update_one({"_id": level_id}, {"$set": {"is_deleted": 1}})
    db.level_comment.delete_many({"level_id": level_id})

    os.remove(join(
        PATH_TO_ROOT, "data", "level", f"{str(level_id)}.level"
    ))

    th = Thread(name="removal_of_residues",
                target=removal_of_residues,
                args=(level_id,))
    th.start()

    return "1"
