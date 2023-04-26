# menuscript/menu/menu.py

import rumps
import controller.controller as controller
from functools import partial
from . import classes
from logger.logger import _log
from controller.controller import Error_, Info_

class MenuBarApp(rumps.App):
    """
    Represents the MenuScripts application, which is a subclass of `rumps.App`.

    :param name: name parameter passed to rumps.App init method.
    :param icon: path to the icon of the app.
    :param items: list of ScriptItem objects loaded from user config file.
    """

    def __init__(self, name: str, icon: str, items: list) -> None:
        super().__init__(name=name, icon=icon, quit_button=None) # type: ignore

        self.items = items
            
        # loads the number of times a script has been executed
        self.num_executions = controller.get_num_executions()
        self.init_menu()

    def init_menu(self) -> None:
        """
        Refreshes the menu bar with items from user config file.

        :params self: the MenuBarApp object.
        """
        
        self.menu.clear()

        if not len(self.items):
            self.menu = [
                rumps.MenuItem(
                    "Add new item",
                    callback=self.add,
                ),
                [
                    rumps.MenuItem("More..."),
                    [
                        rumps.MenuItem("Open editor", callback=self.open_config_file),
                        None,
                        rumps.MenuItem("Raise an issue", callback=self.report_issue),
                        rumps.MenuItem("Documentation", callback=self.read_docs),
                        rumps.MenuItem("Reset application", callback=self.reset_app),
                    ],
                ],
                rumps.MenuItem("Quit", callback=rumps.quit_application),
                rumps.MenuItem(f"Count ({self.num_executions})"),
            ]
            return

        for i, (name, source, interpreter) in enumerate(self.items):
            self.menu.add(rumps.MenuItem(name))
            item = self.menu.get(name)
            callback_item = (name, source, interpreter)

            item.update( # type: ignore
                        self.create_item_menu(f"{i}", callback_item)
            )

        # Add the rest of the menu items
        
        self.menu = [
            None,
            rumps.MenuItem(
                "Add new item",
                callback=self.add,
            ),
            [
                rumps.MenuItem("More..."),
                [
                    rumps.MenuItem("Open editor", callback=self.open_config_file),
                    None,
                    rumps.MenuItem("Raise an issue", callback=self.report_issue),
                    rumps.MenuItem("Documentation", callback=self.read_docs),
                    rumps.MenuItem("Reset application", callback=self.reset_app),
                ],
            ],
            rumps.MenuItem("Quit", callback=rumps.quit_application),
            rumps.MenuItem(f"Count ({self.num_executions})"),
        ]

    def add(self, _):
        """
        Adds a template item to the menu bar. The user can then edit the item without
        using the config file through use of tkinter popup windows.
        """

        new_item = ("Template", "Assign a source", controller.get_global_interpreter())
        
        for item in self.items:
            if item[0] == "Template":
                Info_("To add a new template item, please edit the name of the existing one.")
                return
            
            
        self.items.append(new_item)
        controller.write_item(new_item)
        self.init_menu()

    def execute(self, item: tuple, _):
        """
        Executes the script associated with the item. Tries to execute the script,
        if value error is raised, the script fails to execute and the user is
        notified by the controller.

        :params self: the MenuBarApp object.
        """
        if (
            type(controller.execute(item)) == Exception
        ):  # evaluates to True if script is executed successfully
            return
        self.menu.pop(f"Count ({self.num_executions})")
        self.num_executions = controller.get_num_executions()
        self.menu.add(rumps.MenuItem(f"Count ({self.num_executions})"))

    def edit_name(self, item: tuple, _):
        """
        Opens a popup to edit the name of the item. If the name is valid, the item is
        updated in the .menuscript/config file. Updates the instance variable `items`
        by removing the old item and adding the new item. Then updates the menu to reflect,
        the change without restarting.

        :param self: the MenuBarApp object.
        :param item: the item to be edited.

        """
        old_name = item[0]
        source = item[1]
        interpreter = item[2]

        e = classes.EditName(old_name)
        e.__setattr__("icon", f"{controller.paths.app_path}/imgs/icon.icns")
        response = e.run()

        if not response.clicked == 1 and not response.text != old_name:
            return

        new_name = response.text  # get new name from popup

        r = controller.update_name(
            (old_name, source, interpreter), new_name
        )  # Validate new name

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
        run = old_menu_item.get("Run") # type: ignore

        self.menu.insert_before(
            old_menu_item.__getattribute__("title"),
            rumps.MenuItem(new_name),
        )
        new_top_level_item = self.menu.get(new_name)  # Create new top level menu item
        new_top_level_item.update( # type: ignore
            self.create_item_menu(run.__getattribute__("key"), new_item)
        )
        self.menu.pop(old_name)  # remove old menu item

    def edit_source(self, item: tuple, _):
        """
        Opens a tkinter window stored locally in the .menuscript data file which allows,
        the user to select files locally on their machine. Done outside of the rumps
        program because there are memory management conflicts between Rumps, tkinter,
        and python.

        :params self: the MenuBarApp object.
        """

        name = item[0]
        old_source = item[1]

        new_source = controller.open_filepicker()
        new_source = new_source.removesuffix("\n")  # Format path without newline # type: ignore

        r = controller.update_source(item, new_source)

        if not r or len(self.items) <= 0:  # Valid path was selected
            return
        
        
        for i, (name, source, interpreter) in enumerate(self.items):
            if source == old_source:
                self.items.remove((name, old_source, interpreter))
                break
            
        new_item = (name, new_source, interpreter) # type: ignore
        self.items.append(new_item)

        top_level_item = self.menu.get(name)
        top_level_item.clear() # type: ignore
        top_level_item.update( # type: ignore
            self.create_item_menu(top_level_item.__getattribute__("key"), new_item)
        )

    def edit_interpreter(self, item: tuple, _):
        """
        Opens the user_config.txt file in the default text editor.

        :params self: the MenuBarApp object.
        """
        name = item[0]
        old_interpreter = item[2]

        new_interpreter = controller.open_interpreter_picker()
        new_interpreter = new_interpreter.removesuffix( # type: ignore
            "\n"
        )  # format path without newline

        r = controller.update_interpreter(item, new_interpreter)

        if not r or len(self.items) <= 0 :  # if interpreter is invalid cancel edit
            return

        top_level_item = self.menu.get(name)

        for i, (name, source, interpreter) in enumerate(
            self.items
        ):  # remove old item from self.items
            if interpreter == old_interpreter:
                self.items.remove((name, source, old_interpreter))
                break

        new_item = (name, source, new_interpreter) # type: ignore
        self.items.append(new_item)

        top_level_item = self.menu.get(name)
        top_level_item.clear() # type: ignore
        top_level_item.update( # type: ignore
            self.create_item_menu(top_level_item.__getattribute__("key"), new_item)
        )

    def create_item_menu(self, key: str, item: tuple):
        """
        Creates a new item menu.
        """
        name = item[0]
        source = item[1]
        interpreter = item[2]

        return [
            rumps.MenuItem(
                "Run",
                key=key,
                callback=partial(self.execute, item),
            ),
            None,
            rumps.MenuItem(
                "Schedule job (soon)",
                # callback=partial(controller.schedule_job, self.items[key]),
            ),
            [
                rumps.MenuItem(
                    "Edit",
                    callback=partial(self.edit_name, item),
                ),
                [
                    rumps.MenuItem(
                        f"{controller.get_name_label(name)}",
                        callback=partial(self.edit_name, item),
                    ),
                    rumps.MenuItem(
                        f"{controller.get_source_label(source)}",
                        callback=partial(self.edit_source, item),
                    ),
                    rumps.MenuItem(
                        f"{controller.get_interpreter_label(interpreter)}",
                        callback=partial(self.edit_interpreter, item),
                    ),
                ],
            ],
            rumps.MenuItem("Delete", callback=partial(self.delete, item)),
        ]

    def delete(self, item: tuple, sender):
        """
        Deletes the item from the user_config.txt file.
        """
        if len(self.items) <= 0:
            return
        
        for name, source, interpreter in self.items:
            if (name, source, interpreter) == item:
                self.items.remove(item)
                break

        self.menu.clear()
        controller.remove_item(item)
        self.init_menu()

    def open_config_file(self, _):
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
