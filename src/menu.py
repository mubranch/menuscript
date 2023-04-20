import rumps
from controller import ScriptItem, execute, items_to_dict, open_config, open_url
from functools import partial


class MenuBarApp(rumps.App):
    """
    Represents the MenuScripts application, which is a subclass of `rumps.App`.

    :param name: name parameter passed to rumps.App init method.
    :param icon: path to the icon of the app.
    :param items: list of ScriptItem objects loaded from user_config.txt.
    """

    items = list[ScriptItem]

    def __init__(self, name: str, icon: str, items: list[ScriptItem]) -> None:
        super().__init__(name=name, icon=icon)
        self.items = items_to_dict(items)
        self.init_menu()

    def init_menu(self) -> None:
        """
        Refreshes the menu bar with items from user_config.txt.

        :params self: the MenuBarApp object.
        """

        for key, value in self.items.items():
            rumps.clicked(key)(partial(execute, value))

        self.menu = [
            *self.items,
            None,
            [
                rumps.MenuItem("More"),
                [
                    rumps.MenuItem("Edit Scripts", callback=self.edit_scripts),
                    rumps.MenuItem("Report a Bug", callback=self.report_bug),
                ],
            ],
        ]

    def edit_scripts(self, _):
        """
        Opens the user_config.txt file in the default text editor.

        :params self: the MenuBarApp object.
        """

        rumps.notification(
            title="MenuScript",
            subtitle="Edit Scripts",
            message="Save and Reload the app for changes to take effect.",
        )

        open_config()

    def report_bug(self, _):
        """

        Opens the GitHub issues page in the default browser.

        :params self: the MenuBarApp object.
        """

        open_url()
