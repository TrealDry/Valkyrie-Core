from plugins.plugin import Plugin


def get_plugin(plugin_manager: object) -> object:
    return TestPlugin(plugin_manager)


class TestPlugin(Plugin):
    plugin_name: str = "vcore_test_plugin"

    def plugin_init(self) -> bool:
        print("Test plugin load...")

        return True

    def plugin_destruction(self) -> None:
        print("Goodbye!")

    # == Player events ==

    def on_player_new(self, account_id: int, username: str) -> None:
        print(f"New player! AccountID: {account_id}, Name: {username}")

    def on_player_activate(self, account_id: int, username: str) -> None:
        print(f"New activated account! AccountID: {account_id}, Name: {username}")

    def on_player_login(self, account_id: int, username: str) -> None:
        print(f"Player logged in! AccountID: {account_id}, Name: {username}")

    def on_player_backup(self, account_id: int, username: str) -> None:
        print(f"Player backed up the data! AccountID: {account_id}, Name: {username}")

    def on_player_sync(self, account_id: int, username: str) -> None:
        print(f"Player downloaded the data! AccountID: {account_id}, Name: {username}")

    def on_player_score_update(self, account_id: int, user_stats_before: dict, user_stats_now: dict) -> None:
        print(f"Player has updated his stats! AccountID: {account_id}")
        print(f"Before: {user_stats_before}\nAfter: {user_stats_now}")

    # == ==

    # == Level events ==

    def on_level_upload(self, level_id: int, level_name: str, account_id: int, username: str) -> None:
        print(
            f"A new level from player \"{username}\" (Account ID: {account_id}) has been posted. "
            f"Level name: {level_name}, Level ID: {level_id}"
        )

    def on_level_update(self, level_id: int, level_version: int, account_id: int, username: str) -> None:
        print(
            f"A level update from player \"{username}\" (Account ID: {account_id}) has been released. "
            f"Level ID: {level_id}, Level version: {level_version}"
        )

    def on_level_delete(self, level_id: int, account_id: int) -> None:
        print(
            f"A level has been removed "
            f"Level ID: {level_id}, Author ID: {account_id}"
        )

    def on_level_rate(
            self, level_id: int, level_name: str, builder_id: int, builder_name: str,
            mod_id: int, mod_name: str, role_id: int, is_send: bool, stars: int, feature: int
    ) -> None:
        print(f"Level was {"been sent for rate!" if is_send else "rated!"}\n"
              f"Level name: {level_name}, Level ID: {level_id}\n"
              f"Created by: {builder_name} (Account ID: {builder_id})\n"
              f"Rated by: {mod_name} (Account ID: {mod_id}), Role ID: {role_id}\n"
              f"Stars: {stars}, FeatureID: {feature}")

    def on_level_rate_stars(self, level_id: int, account_id: int, stars: int) -> None:
        print(
            f"Player (Account ID: {account_id}) rated this level (Level ID: {level_id}) {stars} star"
            f"{'' if stars < 2 else 's'}\n", end="", sep=""
        )

    def on_level_rate_demon(self, level_id: int, account_id: int, role_id: int, diff: int) -> None:
        print(
            f"I'm tired... Level ID: {level_id}, Account ID: {account_id}, Is mod: {bool(role_id)}, " +
            f"{f"Role ID: {role_id}, " if bool(role_id) else ""}Demon type: {diff}"
        )

    def on_level_report(self, level_id: int, ip: str) -> None:
        print(f"REPORT! "
              f"IP Address: {ip}, Level ID: {level_id}")

    # == ==

    # == Other events ==

    def on_like_item(self, account_id: int, item_id: int, item_type: int, is_like: bool):
        if item_type == 1:
            item_type_str = "level"
        elif item_type == 2:
            item_type_str = "level comment"
        elif item_type == 3:
            item_type_str = "post"
        else:
            item_type_str = "level list"

        print(
         f"The player (id: {account_id}) {"didn\'t " if not is_like else ""}liked {item_type_str} under id {item_id}"
        )

    # == ==
