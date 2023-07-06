import json
from . import level
from time import time
from os.path import join
from sys import getsizeof
from config import PATH_TO_DATABASE, PATH_TO_ROOT
from utils import passwd, regex, last_id, encoding, check_secret, request_limiter, limit_check, \
    request_get as rg, database as db


maximum_level_size = 10485760  # 10 МБ
minimum_number_blocks = 0


@level.route(f"{PATH_TO_DATABASE}/uploadGJLevel21.php", methods=("POST", "GET"))
def upload_level():
    if not check_secret.main(
        rg.main("secret"), 1
    ):
        return "-1"

    account_id = rg.main("accountID", "int")
    password = rg.main("gjp")

    if not passwd.check_password(
        account_id, password
    ):
        return "-1"

    level_name = regex.char_clean(rg.main("levelName"))
    level_string = rg.main("levelString")

    extra_string = rg.main("extraString")
    level_length = rg.main("levelLength", "int")
    audio_track = rg.main("audioTrack", "int")
    level_desc = rg.main("levelDesc")
    two_player = rg.main("twoPlayer", "int")
    unlisted = rg.main("unlisted", "int")
    password = rg.main("password")
    original = rg.main("original", "int")
    objects = rg.main("objects", "int")
    song_id = rg.main("songID", "int")
    coins = rg.main("coins", "int")
    ldm = rg.main("ldm", "int")

    if getsizeof(level_string) > maximum_level_size:
        return "-1"

    if len(level_name) == 0 or len(level_string) == 0:
        return "-1"

    password = 1 if (password == "1") or (len(password) == 7) else 0

    if not limit_check.main(
        (level_length, 4), (len(encoding.base64_decode(level_desc)), 140), (two_player, 1),
        (unlisted, 1), (len(str(original)), 6), (coins, 3), (ldm, 1), (len(level_name), 20)
    ):
        return "-1"

    if limit_check.main((objects, minimum_number_blocks)) or objects <= 0:
        return "-1"

    if db.song.count_documents({
        "_id": song_id
    }) == 0 and song_id != 0:
        return "-1"

    is_official_song = 1 if song_id <= 0 else 0

    song_id = audio_track if bool(is_official_song) else song_id
    level_id = rg.main("levelID", "int")

    if level_id == 0:
        if not request_limiter.main(
            db.level, {"account_id": account_id}, limit_time=300
        ):
            return "-1"

        level_id = last_id.main(db.level)

        with open(join(
            PATH_TO_ROOT, "data", "level", f"{str(level_id)}.level"
        ), "w") as file:
            file.write(level_string)

        sample_level = {
            "_id": level_id, "account_id": account_id, "username": db.account.find_one({"_id": account_id})["username"],
            "name": level_name, "desc": level_desc, "likes": 0, "downloads": 0, "version": 1, "length": level_length,
            "objects": objects, "password": password, "extra_string": extra_string,
            "coins": coins, "is_silver_coins": 0, "difficulty": 0, "stars": 0, "featured": 0, "epic": 0,
            "auto": 0, "demon": 0, "demon_type": 0, "song_id": song_id, "is_official_song": is_official_song,
            "original_id": original, "two_player": two_player, "unlisted": unlisted, "ldm": ldm, "upload_time": int(time()),
            "update_time": 0, "rate_time": 0, "is_deleted": 0, "delete_prohibition": 0, "update_prohibition": 0
        }

        db.level.insert_one(sample_level)

        return str(level_id)

    elif db.level.count_documents({
        "_id": level_id, "account_id": account_id,
        "update_prohibition": 0, "is_deleted": 0
    }) == 1:
        if not request_limiter.main(
            db.level, {"_id": level_id, "account_id": account_id}, date="update_time", limit_time=300
        ):
            return "-1"

        single_level = tuple(db.level.find({"_id": level_id}))
        level_version = single_level[0]["version"]

        with open(join(
            PATH_TO_ROOT, "data", "level", f"{str(level_id)}.level"
        ), "r") as file:
            old_level_string = file.read()

        with open(join(
            PATH_TO_ROOT, "data", "level", f"{str(level_id)}.level"
        ), "w") as file:
            file.write(level_string)

        with open(join(
            PATH_TO_ROOT, "data", "old_level", f"{str(level_id)}v{level_version}.old.level"
        ), "w") as file:
            file.write(old_level_string)

        with open(join(
                PATH_TO_ROOT, "data", "old_level", f"{str(level_id)}v{level_version}.old.level.db"
        ), "w") as file:
            file.write(json.dumps(single_level[0]))

        db.level.update_one({"_id": level_id}, {"$set": {
            "desc": level_desc,
            "version": level_version + 1,
            "password": password,
            "song_id": song_id,
            "is_official_song": is_official_song,
            "two_player": two_player,
            "objects": objects,
            "coins": coins,
            "extra_string": extra_string,
            "update_time": int(time()),
            "ldm": ldm
        }})

        return str(level_id)

    return "-1"
