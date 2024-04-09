from plugins.plugin_manager import PluginManager


plugin_manager = PluginManager()


def init_plugin_manager():
    plugin_manager.start()
