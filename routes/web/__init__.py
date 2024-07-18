from flask import Blueprint


web = Blueprint('web', __name__)


from .cron import *
from .discord import *
from .song_add_file import *
from .song_add_link import *
from .song_download import *
from .change_prefix import *
from .activate_account import *
