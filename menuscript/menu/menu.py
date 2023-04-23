# menuscript/menu/menu.py

import rumps
import controller.controller as controller
from functools import partial
from .classes import Window


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

        for i, key in enumerate(self.items):
            self.menu.add(rumps.MenuItem(key))
            item = self.menu.get(key)
            name = self.items[key].get("name")

            path = self.items[key].get("source")

            p = str(controller.pathlib.Path(path)).split("/")[-1]
            path = f"Source: '{p}'"

            venv = self.items[key].get("interpreter")

            if venv == "":
                venv = "Interpreter: 'Global'"
            else:
                venv_dir_name = str(controller.pathlib.Path(venv)).split("/")[-3]
                venv_ex_name = str(controller.pathlib.Path(venv)).split("/")[-1]
                venv = f"Interpreter: '({venv_dir_name}) {venv_ex_name}'"

            item.update(
                [
                    rumps.MenuItem(
                        "Run",
                        key=f"{i}",
                        callback=partial(controller.execute, self.items[key]),
                    ),
                    None,
                    rumps.MenuItem(
                        "Schedule",
                        callback=partial(controller.schedule_job, self.items[key]),
                    ),
                    [
                        rumps.MenuItem(
                            "Edit", callback=partial(self.edit, self.items[key])
                        ),
                        [
                            rumps.MenuItem(
                                f"Name: {name}",
                                callback=partial(self.edit, self.items[key]),
                            ),
                            rumps.MenuItem(
                                f"{path}",
                                callback=partial(self.edit_path, self.items[key]),
                            ),
                            rumps.MenuItem(
                                f"{venv}",
                                callback=partial(self.edit_path, self.items[key]),
                            ),
                        ],
                    ],
                ]
            )

        self.menu = [
            None,
            [
                rumps.MenuItem("More..."),
                [
                    rumps.MenuItem("Raise an issue", callback=self.report_issue),
                    rumps.MenuItem("Documentation", callback=self.read_docs),
                    rumps.MenuItem("Reset application", callback=self.reset_app),
                ],
            ],
        ]

    def edit(self, item: controller.ScriptItem, _):
        """
        Opens the user_config.txt file in the default text editor.

        :params self: the MenuBarApp object.
        """
        w = Window()
        w.__setattr__("icon", "menuscript/resources/imgs/icon.icns")
        w.run()

    def edit_path(self, item: controller.ScriptItem, sender):
        """
        Opens the user_config.txt file in the default text editor.

        :params self: the MenuBarApp object.
        """

        if ".py" in sender.title:
            rumps.alert("Change python script.")
        else:
            rumps.alert("Change venv path.")

    def edit_scripts(self, _):
        """
        Opens the user_config.txt file in the default text editor.

        :params self: the MenuBarApp object.
        """

        controller.open_config()

    def report_issue(self, _):
        """
        Opens the GitHub issues page in the default browser.

        :params self: the MenuBarApp object.
        """

        controller.open_url("https://github.com/mubranch/menuscript/issues")

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
