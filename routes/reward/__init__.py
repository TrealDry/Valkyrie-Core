from flask import Blueprint


reward = Blueprint('reward', __name__)


from .get_rewards import *
from .get_challenges import *
from .get_secret_reward import *
