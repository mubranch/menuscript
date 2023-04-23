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

    def __init__(self, name: str, icon: str, items: list) -> None:
        super().__init__(name=name, icon=icon)

        self.items = items
        self.init_menu()

    def init_menu(self) -> None:
        """
        Refreshes the menu bar with items from user_config.txt.

        :params self: the MenuBarApp object.
        """
        if self.items is None or len(self.items) == 0:
            self.menu = [
                rumps.MenuItem(
                    "Add new item",
                    # callback=self.add,
                ),
                [
                    rumps.MenuItem("More..."),
                    [
                        rumps.MenuItem("Bulk edit items", callback=self.bulk_edit),
                        None,
                        rumps.MenuItem("Raise an issue", callback=self.report_issue),
                        rumps.MenuItem("Documentation", callback=self.read_docs),
                        rumps.MenuItem("Reset application", callback=self.reset_app),
                        rumps.MenuItem("Quit", callback=rumps.quit_application),
                    ],
                ],
            ]
            return

        for i, (name, source, interpreter) in enumerate(self.items):
            self.menu.add(rumps.MenuItem(name))
            item = self.menu.get(name)

            name_label = controller.get_name_label(name)
            source_label = controller.get_source_label(source)

            if interpreter is None:
                interpreter_label = "Interpreter: 'Global'"
            else:
                interpreter_label = controller.get_interpreter_label(interpreter)

            item_tuple = (name, source, interpreter)

            item.update(
                [
                    rumps.MenuItem(
                        "Run",
                        key=f"{i}",
                        callback=partial(controller.execute, item_tuple),
                    ),
                    None,
                    rumps.MenuItem(
                        "Schedule job",
                        # callback=partial(controller.schedule_job, self.items[key]),
                    ),
                    [
                        rumps.MenuItem(
                            "Edit",
                            callback=partial(self.edit, item_tuple),
                        ),
                        [
                            rumps.MenuItem(
                                f"{name_label}",
                                callback=partial(self.edit, item_tuple),
                            ),
                            rumps.MenuItem(
                                f"{source_label}",
                                callback=partial(self.edit_source, item_tuple),
                            ),
                            rumps.MenuItem(
                                f"{interpreter_label}",
                                callback=partial(self.edit_interpreter, item_tuple),
                            ),
                        ],
                    ],
                    rumps.MenuItem("Delete", callback=partial(self.delete, item_tuple)),
                ]
            )

        self.menu = [
            None,
            rumps.MenuItem(
                "Add new item",
                # callback=self.add,
            ),
            [
                rumps.MenuItem("More..."),
                [
                    rumps.MenuItem("Bulk edit items", callback=self.bulk_edit),
                    None,
                    rumps.MenuItem("Raise an issue", callback=self.report_issue),
                    rumps.MenuItem("Documentation", callback=self.read_docs),
                    rumps.MenuItem("Reset application", callback=self.reset_app),
                ],
            ],
        ]

    def add(self, item: tuple, _):
        ...

    def edit(self, item: tuple, _):
        """
        Open a dialog to edit the name of the item.
        Removes the old item from self.items and adds the new item.
        Passes the new item to controller.update_name() to update the user_config.txt file.
        After updating the user_config.txt file, the menu bar is refreshed.

        :params self: the MenuBarApp object.
        """
        old_name = item[0]
        source = item[1]
        interpreter = item[2]

        e = classes.EditName(old_name)
        e.__setattr__("icon", f"{controller.settings.app_path}/imgs/icon.icns")
        response = e.run()

        if response.clicked and response.text != old_name:
            new_name = response.text
            top_level_item = self.menu.get(old_name)

            r = controller.update_name((old_name, source, interpreter), new_name)

            if not r:
                return

            for name, source, interpreter in self.items:
                if name == old_name:
                    self.items.remove((old_name, source, interpreter))
                    break

            new_item = (new_name, source, interpreter)
            self.items.extend(new_item)

            top_level_item.__setattr__("title", new_name)
            top_level_item.set_callback(
                callback=partial(controller.execute, new_item),
                key=top_level_item.__getattribute__("key"),
            )
            sub_menu = top_level_item["Edit"]
            sub_menu.get(controller.get_name_label(old_name)).__setattr__(
                "title", controller.get_name_label(new_name)
            )

    def edit_source(self, item: tuple, sender):
        """
        Opens the user_config.txt file in the default text editor.

        :params self: the MenuBarApp object.
        """
        name = item[0]
        source = item[1]

        new_source = controller.open_filepicker()
        new_source = new_source.removesuffix("\n")
        r = controller.update_source(item, new_source)

        if not r:
            return

        for name, source, interpreter in self.items:
            if source == source:
                self.items.remove((source, source, interpreter))
                break

        new_item = (name, new_source, interpreter)
        self.items.extend(new_item)

        top_level_item = self.menu.get(name)
        sub_menu = top_level_item["Edit"]
        sub_menu.get(controller.get_source_label(source)).__setattr__(
            "title", controller.get_source_label(new_source)
        )

    def edit_interpreter(self, item: tuple, _):
        """
        Opens the user_config.txt file in the default text editor.

        :params self: the MenuBarApp object.
        """
        name = item[0]
        interpreter = item[2]

        new_interpreter = controller.open_interpreter_picker()
        new_interpreter = new_interpreter.removesuffix("\n")
        r = controller.update_interpreter(item, new_interpreter)

        if not r:
            return

        for name, source, interpreter in self.items:
            if interpreter == interpreter:
                self.items.remove((name, source, interpreter))
                break

        new_item = (name, source, new_interpreter)
        self.items.extend(new_item)

        top_level_item = self.menu.get(name)
        sub_menu = top_level_item["Edit"]
        sub_menu.get(controller.get_interpreter_label(interpreter)).__setattr__(
            "title", controller.get_interpreter_label(new_interpreter)
        )

    def delete(self, item: tuple, sender):
        """
        Deletes the item from the user_config.txt file.
        """
        for name, source, interpreter in self.items:
            if (name, source, interpreter) == item:
                self.items.remove(item)
                break

        top_level_item = self.menu.get(name)
        controller.remove_item(top_level_item)
        self.menu.clear()
        self.init_menu()

    def bulk_edit(self, _):
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
