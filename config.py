from loguru import logger
from os import getcwd, getenv
from utils.load_config import LoadConfig, LoadConfigResponse as LCEnum

conf_dict = dict()
path_to_config = getenv("path_to_config")

if not path_to_config:
    logger.warning("Не указан путь к конфигу! Автоматически выбран standard.config.json.")

load_status = LoadConfig.load_config(
    path_to_config, conf_dict
)

match load_status:
    case LCEnum.DONE:            logger.debug(f"Файл конфигурации загружен успешно! path={path_to_config}")
    case LCEnum.FILE_NOT_FOUND:  logger.critical(f"Файл конфига не был найден! path={path_to_config}");         raise Exception
    case LCEnum.STRUCTURE_ERROR: logger.critical(f"Структура конфига повреждена! path={path_to_config}");       raise Exception
    case LCEnum.UNKNOWN_ERROR:   logger.critical(f"Неизвестная ошибка! Проверьте файл! path={path_to_config}"); raise Exception

# == Server settings ==

GD_SERVER_NAME      = conf_dict["server_setts_name"]
DISCORD_SERVER_LINK = conf_dict["server_setts_discord_link"]

DOMAIN              = conf_dict["server_setts_domain"]

PATH_TO_API         = conf_dict["server_setts_path_to_api"]
PATH_TO_ROOT        = getcwd()
PATH_TO_SONG        = conf_dict["server_setts_path_to_song"]
PATH_TO_DATABASE    = conf_dict["server_setts_path_to_database"]

COMMAND_PREFIX      = conf_dict["server_setts_command_prefix"]

MAX_CONTENT_LENGTH  = conf_dict["server_setts_max_content_length"]

# == ==

# == Secret settings ==

MAIL_SERVER   = conf_dict["secret_setts_mail_ip"]
MAIL_USERNAME = conf_dict["secret_setts_mail_username"]
MAIL_PASSWORD = conf_dict["secret_setts_mail_password"]
MAIL_PORT     = conf_dict["secret_setts_mail_port"]

MONGO_URI     = conf_dict["secret_setts_mongo_uri"]
MONGO_NAME    = conf_dict["secret_setts_mongo_db_name"]

REDIS_HOST     = conf_dict["secret_setts_redis_ip"]
REDIS_PORT     = conf_dict["secret_setts_redis_port"]
REDIS_PASSWORD = conf_dict["secret_setts_redis_password"]
REDIS_PREFIX   = conf_dict["secret_setts_redis_prefix"]

HCAPTCHA_SITE_KEY   = conf_dict["secret_setts_hcaptcha_site_key"]
HCAPTCHA_SECRET_KEY = conf_dict["secret_setts_hcaptcha_secret_key"]

# == ==

# == Security settings ==

ACCOUNTS_ACTIVATION_VIA_MAIL    = conf_dict["security_setts_accounts_activation_via_mail"]
PROTECTION_AGAINST_DISLIKE_BOTS = conf_dict["security_setts_dislike_bot_protection"]

# == ==

# == Debug settings ==

IP    = conf_dict["debug_setts_host_ip"]
PORT  = conf_dict["debug_setts_host_port"]
DEBUG = conf_dict["debug_setts_flask_debug"]

# == ==
