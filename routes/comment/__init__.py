from flask import Blueprint


comment = Blueprint('comment', __name__)


from .get_comments import *
from .upload_comment import *
from .delete_comment import *
from .get_comment_history import *
from .get_account_comments import *
from .upload_account_comment import *
from .delete_account_comment import *
