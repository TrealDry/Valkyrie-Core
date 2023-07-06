from flask import Blueprint


level_pack = Blueprint('level_pack', __name__)


from .get_gauntlets import *
from .get_map_packs import *
