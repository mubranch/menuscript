# menuscript/menu/menu.py

import rumps
import controller.controller as controller
from functools import partial
from . import classes


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

            name_label = f"Name: {name}"

            source = self.items[key].get("source")

            s = str(controller.pathlib.Path(source)).split("/")[-1]
            source_label = f"Source: '{s}'"

            interpreter = self.items[key].get("interpreter")

            if interpreter == "":
                interpreter_label = "Interpreter: 'Global'"
            else:
                i_dir_name = str(controller.pathlib.Path(interpreter)).split("/")[-3]
                i_ex_name = str(controller.pathlib.Path(interpreter)).split("/")[-1]
                interpreter_label = f"Interpreter: '({i_dir_name}) {i_ex_name}'"

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
                                f"{name_label}",
                                callback=partial(self.edit, self.items[key]),
                            ),
                            rumps.MenuItem(
                                f"{source_label}",
                                # callback=partial(self.edit_path, self.items[key]),
                            ),
                            rumps.MenuItem(
                                f"{interpreter_label}",
                                # callback=partial(self.edit_path, self.items[key]),
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

    def edit(self, item: dict, _):
        """
        Opens the user_config.txt file in the default text editor.

        :params self: the MenuBarApp object.
        """
        old_name = item.get("name")

        e = classes.EditName(old_name)
        e.__setattr__("icon", f"{controller.settings.app_path}/imgs/icon.icns")
        response = e.run()

        if response.clicked:
            new_name = response.text
            top_level_item = self.menu.get(old_name)
            controller.update_name(self.items.get(old_name), new_name)
            top_level_item.__setattr__("title", new_name)
            sub_menu = top_level_item["Edit"]
            sub_menu.get(f"Name: {old_name}").__setattr__("title", f"Name: {new_name}")

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
