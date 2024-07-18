from . import web
from flask import redirect
from config import DISCORD_SERVER_LINK


@web.route("/discord")
def discord():
    return redirect(DISCORD_SERVER_LINK)
