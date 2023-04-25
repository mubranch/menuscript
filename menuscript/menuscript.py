#!/menuscript/menuscript.py

from menu.menu import MenuBarApp
import controller.controller as controller
import resources.settings as settings
import pathlib
import logging




def main():
    settings.init()

    items = controller.load_items()

    menu = MenuBarApp(
        name="MenuScript",
        icon=str(pathlib.Path(f"{settings.image_path}/light.icns")),
        items=items,
    )

    menu.run()
    logging.info("MenuScript started")


if __name__ == "__main__":
    main()
    logging.info("MenuScript ended")
