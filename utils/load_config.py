import json
from enum import Enum


class LoadConfigResponse(Enum):
    DONE             = 0
    FILE_NOT_FOUND   = 1
    STRUCTURE_ERROR  = 2
    UNKNOWN_ERROR    = 3

class LoadConfig:

    @staticmethod
    def __json_parsing(json_dict: dict, dict_name: str, save_to_dict: dict) -> None:
        for key, value in json_dict.items():
            element_name = f"{dict_name}_{key}" if dict_name else key

            if isinstance(value, dict):
                LoadConfig.__json_parsing(
                    value, element_name, save_to_dict
                )
                continue

            save_to_dict[element_name] = value

    @staticmethod
    def load_config(path: str, save_to_dict: dict) -> LoadConfigResponse:
        if not path:
            path = ".\\configs\\standard.config.json"

        try:
            with open(path, "r") as file:
                config_json = json.load(file)
        except FileNotFoundError:    return LoadConfigResponse.FILE_NOT_FOUND
        except json.JSONDecodeError: return LoadConfigResponse.STRUCTURE_ERROR
        except:                      return LoadConfigResponse.UNKNOWN_ERROR

        LoadConfig.__json_parsing(config_json, "", save_to_dict)

        return LoadConfigResponse.DONE
