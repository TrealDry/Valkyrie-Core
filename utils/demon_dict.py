from loguru import logger
from config import REDIS_PREFIX
from routes.web.cron import update_demon_list

from utils.redis_db import client as rd


def get_demon_dict() -> dict:
    while True:
        demon_list = rd.get(f"{REDIS_PREFIX}:all_demons")

        if demon_list is None:
            update_demon_list()
            continue
        break

    if demon_list == "":
        return dict()

    demon_list = demon_list.split(";")
    demon_dict = {}

    for i in demon_list:
        i = list(map(int, i.split("-")))
        demon_dict[i[0]] = (i[1], i[2])

    return demon_dict
