# menuscript/menuscript.py

from menu.menu import MenuBarApp
import controller.controller as controller
import resources.settings as settings
import os


def main():
    settings.init()

    items = controller.load_items()

    menu = MenuBarApp(
        name="MenuScript",
        icon=os.path.join(settings.image_path, "light.icns"),
        items=items,
    )

    menu.run()


if __name__ == "__main__":
    main()
