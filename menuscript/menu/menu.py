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
        super().__init__(name=name, icon=icon, quit_button=None)

        self.items = items
        self.number_of_executions = controller.load_executions()
        self.init_menu()

    def init_menu(self) -> None:
        """
        Refreshes the menu bar with items from user_config.txt.

        :params self: the MenuBarApp object.
        """
        if self.menu is not None:
            self.menu.clear()

        if self.items is None or len(self.items) == 0:
            self.items = []
            self.menu = [
                rumps.MenuItem(
                    "Add new item",
                    callback=self.add,
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
                rumps.MenuItem("Quit", callback=rumps.quit_application),
                rumps.MenuItem(f"Count ({self.number_of_executions})"),
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
                        callback=partial(self.execute, item_tuple),
                    ),
                    None,
                    rumps.MenuItem(
                        "Schedule job",
                        # callback=partial(controller.schedule_job, self.items[key]),
                    ),
                    [
                        rumps.MenuItem(
                            "Edit",
                            callback=partial(self.edit_name, item_tuple),
                        ),
                        [
                            rumps.MenuItem(
                                f"{name_label}",
                                callback=partial(self.edit_name, item_tuple),
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
                callback=self.add,
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
            rumps.MenuItem("Quit", callback=rumps.quit_application),
            rumps.MenuItem(f"Count ({self.number_of_executions})"),
        ]

    def add(self, _):
        new_item = ("Template", "Assign a source", None)
        self.items.append(new_item)
        controller.write_item(new_item)
        self.init_menu()

    def execute(self, item: tuple, _):
        """
        Executes the item.

        :params self: the MenuBarApp object.
        """
        controller.execute(item)
        self.menu.pop(f"Count ({self.number_of_executions})")
        self.number_of_executions = controller.load_executions()
        self.menu.add(rumps.MenuItem(f"Count ({self.number_of_executions})"))

    def edit_name(self, item: tuple, _):
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

        if not response.clicked == 1 and not response.text != old_name:
            return

        new_name = response.text  # get new name

        r = controller.update_name(
            (old_name, source, interpreter), new_name
        )  # validate new name

        if not r:  # if name is invalid cancel edit
            return

        for i, (name, source, interpreter) in enumerate(
            self.items
        ):  # remove old item from self.items
            if name == old_name:
                self.items.remove((old_name, source, interpreter))
                break

        new_item = (new_name, source, interpreter)  # create new item
        self.items.append(new_item)  # add new item to self.items

        old_menu_item = self.menu.get(
            old_name
        )  # remove old menu item or live refresh will not work
        run = old_menu_item.get("Run")

        self.menu.insert_before(
            old_menu_item.__getattribute__("title"),
            rumps.MenuItem(new_name),
        )  # insert new menu item
        new_top_level_item = self.menu.get(new_name)
        new_top_level_item.update(
            [
                rumps.MenuItem(
                    "Run",
                    key=run.__getattribute__("key"),
                    callback=partial(self.execute, new_item),
                ),
                None,
                rumps.MenuItem(
                    "Schedule job",
                    # callback=partial(controller.schedule_job, self.items[key]),
                ),
                [
                    rumps.MenuItem(
                        "Edit",
                        callback=partial(self.edit_name, new_item),
                    ),
                    [
                        rumps.MenuItem(
                            f"{controller.get_name_label(new_name)}",
                            callback=partial(self.edit_name, new_item),
                        ),
                        rumps.MenuItem(
                            f"{controller.get_source_label(source)}",
                            callback=partial(self.edit_source, new_item),
                        ),
                        rumps.MenuItem(
                            f"{controller.get_interpreter_label(interpreter)}",
                            callback=partial(self.edit_interpreter, new_item),
                        ),
                    ],
                ],
                rumps.MenuItem("Delete", callback=partial(self.delete, new_item)),
            ],
        )
        self.menu.pop(old_name)  # remove old menu item

    def edit_source(self, item: tuple, sender):
        """
        Opens the user_config.txt file in the default text editor.

        :params self: the MenuBarApp object.
        """
        name = item[0]
        old_source = item[1]

        new_source = controller.open_filepicker()
        new_source = new_source.removesuffix("\n")  # format path without newline

        r = controller.update_source(item, new_source)

        if not r:  # if source is invalid cancel edit
            return

        top_level_item = self.menu.get(name)

        for i, (name, source, interpreter) in enumerate(self.items):
            if source == old_source:
                self.items.remove((name, old_source, interpreter))
                break

        new_item = (name, new_source, interpreter)
        self.items.append(new_item)

        top_level_item = self.menu.get(name)
        top_level_item.clear()
        top_level_item.update(  # build new top level menu item
            [
                rumps.MenuItem(
                    "Run",
                    key=top_level_item.__getattribute__("key"),
                    callback=partial(self.execute, new_item),
                ),
                None,
                rumps.MenuItem(
                    "Schedule job",
                    # callback=partial(controller.schedule_job, self.items[key]),
                ),
                [
                    rumps.MenuItem(
                        "Edit",
                        callback=partial(self.edit_name, new_item),
                    ),
                    [
                        rumps.MenuItem(
                            f"{controller.get_name_label(name)}",
                            callback=partial(self.edit_name, new_item),
                        ),
                        rumps.MenuItem(
                            f"{controller.get_source_label(new_source)}",
                            callback=partial(self.edit_source, new_item),
                        ),
                        rumps.MenuItem(
                            f"{controller.get_interpreter_label(interpreter)}",
                            callback=partial(self.edit_interpreter, new_item),
                        ),
                    ],
                ],
                rumps.MenuItem("Delete", callback=partial(self.delete, new_item)),
            ]
        )

    def edit_interpreter(self, item: tuple, _):
        """
        Opens the user_config.txt file in the default text editor.

        :params self: the MenuBarApp object.
        """
        name = item[0]
        old_interpreter = item[2]

        new_interpreter = controller.open_interpreter_picker()
        new_interpreter = new_interpreter.removesuffix(
            "\n"
        )  # format path without newline

        r = controller.update_interpreter(item, new_interpreter)

        if not r:  # if interpreter is invalid cancel edit
            return

        top_level_item = self.menu.get(name)

        for i, (name, source, interpreter) in enumerate(
            self.items
        ):  # remove old item from self.items
            if interpreter == old_interpreter:
                self.items.remove((name, source, old_interpreter))
                break

        new_item = (name, source, new_interpreter)
        self.items.extend(new_item)  # add new item to self.items

        top_level_item = self.menu.get(name)
        top_level_item.clear()
        top_level_item.update(  # build new top level menu item
            [
                rumps.MenuItem(
                    "Run",
                    key=top_level_item.__getattribute__("key"),
                    callback=partial(self.execute, new_item),
                ),
                None,
                rumps.MenuItem(
                    "Schedule job",
                    # callback=partial(controller.schedule_job, self.items[key]),
                ),
                [
                    rumps.MenuItem(
                        "Edit",
                        callback=partial(self.edit_name, new_item),
                    ),
                    [
                        rumps.MenuItem(
                            f"{controller.get_name_label(name)}",
                            callback=partial(self.edit_name, new_item),
                        ),
                        rumps.MenuItem(
                            f"{controller.get_source_label(source)}",
                            callback=partial(self.edit_source, new_item),
                        ),
                        rumps.MenuItem(
                            f"{controller.get_interpreter_label(new_interpreter)}",
                            callback=partial(self.edit_interpreter, new_item),
                        ),
                    ],
                ],
                rumps.MenuItem("Delete", callback=partial(self.delete, new_item)),
            ]
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
