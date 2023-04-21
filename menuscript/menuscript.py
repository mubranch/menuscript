from menu.menu import MenuBarApp
from controller.controller import load_items, open_url, disable
import settings
import os


def main():
    settings.init()

    items = load_items()

    if settings.first_start:
        open_url()
        disable()

    menu = MenuBarApp(
        name="MenuScript",
        icon=os.path.join(settings.image_path, "light.icns"),
        items=items,
    )

    menu.run()


if __name__ == "__main__":
    main()
