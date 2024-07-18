from flask import Blueprint


message = Blueprint('message', __name__)


from .get_messages import *
from .upload_message import *
from .delete_messages import *
from .download_message import *
