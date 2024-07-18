from flask import Blueprint


user = Blueprint('user', __name__)


from .get_users import *
from .get_user_info import *
from .update_user_score import *
from .update_account_settings import *
