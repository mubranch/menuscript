#!/menuscript/menuscript.py

from menu.menu import MenuBarApp
import controller.controller as controller
import resources.settings as settings
import pathlib


def main():
    settings.init()

    items = controller.load_items()

    menu = MenuBarApp(
        name="MenuScript",
        icon=str(pathlib.Path(f"{settings.image_path}/light.icns")),
        items=items,
    )

    menu.run()


if __name__ == "__main__":
    main()
