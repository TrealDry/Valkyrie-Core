from flask import Blueprint


level = Blueprint('level', __name__)


from .get_level import *
from .rate_demon import *
from .rate_stars import *
from .update_desc import *
from .delete_level import *
from .upload_level import *
from .suggest_stars import *
from .download_level import *
from .get_daily_level import *
