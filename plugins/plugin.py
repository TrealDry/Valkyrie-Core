class Plugin:
    plugin_name: str = ""

    def plugin_init(self) -> bool:
        return True

    def plugin_destruction(self) -> None:
        pass
