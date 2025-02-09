from dotenv import load_dotenv
from os import getcwd, listdir, getenv


env_is_not_exist = True

for file in listdir(r"."):
    if file == ".env":
        load_dotenv()
        env_is_not_exist = False
        break
    else:
        continue


def env(key, type_, default=None):
    if env_is_not_exist:
        return default

    env_value = getenv(key)

    if env_value is None:
        print(f"КЛЮЧ {key} НЕ БЫЛ НАЙДЕЙ!")
        return default

    if type_ == str:
        return env_value
    elif type_ == int:
        try:
            return int(env_value)
        except ValueError:
            print(f"КЛЮЧ {key} НЕ МОЖЕТ БЫТЬ ПРЕОБРАЗОВАН В INT!")
            return default
    else:
        return env_value


# == Server settings ==

IP = "0.0.0.0"
PORT = "80"
DEBUG = False

MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB max

GD_SERVER_NAME = "Geometry Dash Private Server"
DISCORD_SERVER_LINK = "https://discord.com/"

DOMAIN = "https://localhost:5000"

PATH_TO_API = "/api"
PATH_TO_ROOT = getcwd()
PATH_TO_SONG = DOMAIN + "/song"
PATH_TO_DATABASE = "/database/db"

COMMAND_PREFIX = "!"

# == ==

# == Secret settings ==

ACCOUNTS_ACTIVATION_VIA_MAIL = False

MAIL_SERVER = env("MAIL_SERVER", str, "")  # only TLS
MAIL_USERNAME = env("MAIL_USERNAME", str, "")
MAIL_PASSWORD = env("MAIL_PASSWORD", str, "")
MAIL_PORT = env("MAIL_PORT", int, 27017)

MONGO_URI = env("MONGO_URI", str, "mongodb://mongo:27017")
MONGO_NAME = env("MONGO_NAME", str, "vcore")

REDIS_HOST = env("REDIS_HOST", str, "localhost")
REDIS_PORT = env("REDIS_PORT", int, 6379)
REDIS_PASSWORD = env("REDIS_PASSWORD", str, "")
REDIS_PREFIX = "EUPH"

HCAPTCHA_SITE_KEY = env("HCAPTCHA_SITE_KEY", str, "")
HCAPTCHA_SECRET_KEY = env("HCAPTCHA_SECRET_KEY", str, "")

# == ==

# == Security settings ==

LOG_STATUS = 0  # 0 - выключить логирование
# 1 - логирование только ошибок
# 2 - логирование ошибок и предупреждений
# 3 - логирование всего

LOGURU_STATUS = 0

PROTECTION_AGAINST_DISLIKE_BOTS = False  # включить её только в крайнем случае!!!
# При True в like_item проходит проверка (только для уровней).
# Если уровень не был ранее загружен пользователем, то не изменять счётчик лайков.

DISCORD_CONFIRMATION = False  # В некоторых эндпоитнах (напр. Добавление музыки)
# Будет требоваться привязка дискорд аккаунта к гд аккаунту

# == ==
