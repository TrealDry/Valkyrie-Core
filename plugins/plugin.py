class Plugin:
    plugin_name = ""

    def plugin_init(self) -> bool:
        return True

    def plugin_destruction(self):
        pass
