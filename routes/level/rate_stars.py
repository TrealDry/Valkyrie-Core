from . import level
from config import PATH_TO_DATABASE


@level.route(f"{PATH_TO_DATABASE}/rateGJStars211.php", methods=("POST", "GET"))
def rate_stars():
    return "1"  # Заглушка
