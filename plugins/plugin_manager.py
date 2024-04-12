import os
import inspect
import os.path
import colorama
import importlib
from typing import Any


colorama.init()


class PluginManager:
    def __init__(self):
        self.main_folder = os.path.join(".", "plugins")

        self._plugin_space = {}  # Ключ: имя плагина, значение: объект
        self._plugin_paths = {}  # Ключ: имя плагина, значение: путь к плагину
        self._plugin_methods = self.__init_plugin_methods()

    def start(self):
        self.__auto_load_plugins()

    @staticmethod
    def __init_plugin_methods() -> dict:
        return {
            "on_player_new": [],
            "on_player_activate": [],
            "on_player_login": [],
            "on_player_backup": [],
            "on_player_sync": [],
            "on_player_score_update": [],
            "on_level_upload": [],
            "on_level_update": [],
            "on_level_delete": [],
            "on_level_rate": [],
            "on_level_rate_stars": [],
            "on_level_rate_demon": [],
            "on_level_report": [],
            "on_like_item": []
        }

    @staticmethod
    def __init_plugin(plugin_object: Any) -> bool:
        return plugin_object.plugin_init()

    @staticmethod
    def __print_plugin_load_status(plugin_name: str, is_successfully: bool) -> None:
        if is_successfully:
            print(colorama.Fore.GREEN + f"Плагин {plugin_name} успешно загружен!" + colorama.Style.RESET_ALL)
        else:
            print(colorama.Fore.RED + f"Плагин {plugin_name} не был загружен!" + colorama.Style.RESET_ALL)

    def __plugin_methods_entry(self, plugin_name: str) -> None:
        plugin_object = self._plugin_space[plugin_name]
        plugin_methods = [m[0] for m in inspect.getmembers(plugin_object, predicate=inspect.ismethod)]

        for plugin_method in plugin_methods:

            if plugin_method not in self._plugin_methods:
                continue

            self._plugin_methods[plugin_method].append(
                (getattr(plugin_object, plugin_method), plugin_name)
            )

    def __clear_plugin_methods(self, plugin_name: str) -> None:
        delete_list = []

        for i in self._plugin_methods:
            for j in range(len(self._plugin_methods[i])):
                if self._plugin_methods[i][j][1] != plugin_name:
                    continue

                delete_list.append([i, j])

        for i in delete_list:
            del self._plugin_methods[i[0]][i[1]]

    def call_event(self, event_name: str, *args) -> None:
        for i in self._plugin_methods[event_name]:
            i[0](*args)

    def call_method(self, plugin_name: str, method_name: str, *args) -> Any:
        return getattr(self._plugin_space[plugin_name], method_name)(*args)

    def get_plugin_object(self, plugin_name: str) -> Any:
        try:
            return self._plugin_space[plugin_name]
        except IndexError:
            return None

    def is_plugin_exist(self, plugin_name: str) -> bool:
        return plugin_name in self._plugin_space

    def unload_plugin(self, plugin_name: str) -> bool:
        try:
            self._plugin_space[plugin_name].plugin_destruction()
            self.__clear_plugin_methods(plugin_name)
            del self._plugin_space[plugin_name]
            del self._plugin_paths[plugin_name]

            return True
        except KeyError:
            return False

    def load_plugin(self, plugin_path: str) -> str:
        plugin_module_name = plugin_path[2:].replace(os.sep, ".")
        plugin_module = importlib.import_module(plugin_module_name)

        plugin_object = plugin_module.get_plugin(self)
        plugin_name = plugin_object.plugin_name

        result = self.__init_plugin(plugin_object)

        if not result:
            self.__print_plugin_load_status(plugin_name, False)
            return ""

        self._plugin_space[plugin_name] = plugin_object
        self._plugin_paths[plugin_name] = plugin_path
        self.__plugin_methods_entry(plugin_name)

        self.__print_plugin_load_status(plugin_name, True)

        return plugin_name

    def reload_plugin(self, plugin_name: str) -> bool:
        plugin_path = self._plugin_paths[plugin_name]

        if not self.unload_plugin(plugin_name):
            return False

        result = self.load_plugin(plugin_path)
        return bool(result)

    def get_plugin_space(self) -> dict:
        return self._plugin_space

    def get_plugin_path(self) -> dict:
        return self._plugin_methods

    def __auto_load_plugins(self):
        plugin_collections = list(filter(
            os.path.isdir, list(map(lambda x: os.path.join(self.main_folder, x), os.listdir(self.main_folder)))
        ))

        for plugin_coll in plugin_collections:
            plugins = list(filter(
                os.path.isdir, list(map(lambda x: os.path.join(plugin_coll, x), os.listdir(plugin_coll)))
            ))

            for plugin_path in plugins:
                if "__init__.py" not in os.listdir(plugin_path):
                    continue

                self.load_plugin(plugin_path)
