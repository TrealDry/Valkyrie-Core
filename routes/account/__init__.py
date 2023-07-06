from flask import Blueprint


account = Blueprint('account', __name__)

from .login_account import *
from .register_account import *
