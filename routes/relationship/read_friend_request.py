from . import relationship
from config import PATH_TO_DATABASE


@relationship.route(f"{PATH_TO_DATABASE}/readGJFriendRequest20.php", methods=("POST", "GET"))
def read_friend_request():
    return "1"

