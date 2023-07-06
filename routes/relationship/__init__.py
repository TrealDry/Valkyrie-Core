from flask import Blueprint


relationship = Blueprint('relationship', __name__)


from .block_user import *
from .unblock_user import *
from .remove_friend import *
from .get_user_list import *
from .get_friend_requests import *
from .read_friend_request import *
from .upload_friend_request import *
from .accept_friend_request import *
from .delete_friend_requests import *
