import json
from enum import Enum
from flask import Flask


class LoadConfigResponse(Enum):
    DONE             = 0
    FILE_NOT_FOUND   = 1
    STRUCTURE_ERROR  = 2


class LoadConfig:
    rule_exceptions = {
        "server_setts_max_content_length": "MAX_CONTENT_LENGTH",

        "debug_setts_host_ip": "IP",
        "debug_setts_host_port": "PORT",
        "debug_setts_flask_debug": "DEBUG"
    }

    @staticmethod
    def __json_parsing(json_dict: dict, dict_name: str, app: Flask) -> None:
        for key, value in json_dict.items():
            element_name = f"{dict_name}_{key}" if dict_name else key

            if isinstance(value, dict):
                LoadConfig.__json_parsing(
                    value, element_name, app
                )
                continue

            if element_name in LoadConfig.rule_exceptions:
                element_name = LoadConfig.rule_exceptions[element_name]

            app.config[element_name] = value

    @staticmethod
    def load_config(path: str, app: Flask) -> LoadConfigResponse:
        if not path:
            path = ".\\configs\\standard.config.json"

        with open(path, "r") as file:
            config_json = json.load(file)

        LoadConfig.__json_parsing(config_json, "", app)

        return LoadConfigResponse.DONE
