from routes import *
from os import getenv
from flask import Flask
from os.path import join
from loguru import logger

log_level = getenv("log_level")
if not log_level:
    log_level = "DEBUG"

logger.add(
    join("data", "log", "logs.log"),
    format="{time} => {level} => {name}:{function} => {message}",
    level=getenv("log_level"), rotation="64 KB",
    compression="zip"
)

from utils import hcaptcha, plugin_manager
from config import IP, PORT, DEBUG, MAX_CONTENT_LENGTH


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
logger.debug("Flask приложение было создано")

for route in (
    account, comment, level, level_pack, message,
    misc, relationship, reward, score, user, web
):
    app.register_blueprint(route)

hcaptcha.init_hc(app)
logger.debug("Капча была инициализирована")
plugin_manager.init_plugin_manager()
logger.debug("Менеджер плагинов был инициализирован")

if __name__ == "__main__":
    app.run(
        host=IP,
        port=PORT,
        debug=DEBUG
    )
