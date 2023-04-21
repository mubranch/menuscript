import rumps
import controller.controller as controller
from functools import partial


class MenuBarApp(rumps.App):
    """
    Represents the MenuScripts application, which is a subclass of `rumps.App`.

    :param name: name parameter passed to rumps.App init method.
    :param icon: path to the icon of the app.
    :param items: list of ScriptItem objects loaded from user_config.txt.
    """

    items = list[controller.ScriptItem]

    def __init__(
        self, name: str, icon: str, items: list[controller.ScriptItem]
    ) -> None:
        super().__init__(name=name, icon=icon)

        self.items = controller.items_to_dict(items)
        self.init_menu()

    def init_menu(self) -> None:
        """
        Refreshes the menu bar with items from user_config.txt.

        :params self: the MenuBarApp object.
        """

        if self.items is not None:
            for key, value in self.items.items():
                rumps.clicked(key)(partial(controller.execute, value))

            self.menu = [
                *self.items,
                None,
                rumps.MenuItem("Edit Scripts", callback=self.edit_scripts),
                rumps.MenuItem("Documentation", callback=self.read_docs),
                [
                    rumps.MenuItem("More..."),
                    [
                        rumps.MenuItem("Reset", callback=self.reset_app),
                    ],
                ],
            ]
            return

        self.menu = [
            None,
            rumps.MenuItem("Edit Scripts", callback=self.edit_scripts),
            rumps.MenuItem("Documentation", callback=self.read_docs),
            [
                rumps.MenuItem("More..."),
                [
                    rumps.MenuItem("Reset", callback=self.reset_app),
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

        controller.open_config()

    def report_bug(self, _):
        """

        Opens the GitHub issues page in the default browser.

        :params self: the MenuBarApp object.
        """

        controller.open_url("https://www.github.com/mubranch/menuscript")

    def read_docs(self, _):
        """

        Opens the GitHub issues page in the default browser.

        :params self: the MenuBarApp object.
        """

        controller.open_url("https://www.github.com/mubranch/menuscript")

    def reset_app(self, _):
        """

        Resets the MenuScript app.

        :params self: the MenuBarApp object.

        """

        controller.reset()
