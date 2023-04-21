from menu.menu import MenuBarApp
import controller.controller as controller
import settings
import os


def main():
    settings.init()

    items = controller.load_items()

    if settings.first_start:
        controller.open_url()
        controller.disable()

    menu = MenuBarApp(
        name="MenuScript",
        icon=os.path.join(settings.image_path, "light.icns"),
        items=items,
    )

    menu.run()


if __name__ == "__main__":
    main()
