class Plugin:
    plugin_name: str = ""
    plugin_manager: object = None

    def __init__(self, plugin_manager: object) -> None:
        self.plugin_manager = plugin_manager

    def plugin_init(self) -> bool:
        return True

    def plugin_destruction(self) -> None:
        pass
