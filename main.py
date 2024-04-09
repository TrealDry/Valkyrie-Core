from routes import *
from flask import Flask
from utils import hcaptcha, plugin_manager
from config import IP, PORT, DEBUG, MAX_CONTENT_LENGTH


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

for route in (
    account, comment, level, level_pack, message,
    misc, relationship, reward, score, user, web
):
    app.register_blueprint(route)

hcaptcha.init_hc(app)
plugin_manager.init_plugin_manager()

if __name__ == "__main__":
    app.run(
        host=IP,
        port=PORT,
        debug=DEBUG
    )
