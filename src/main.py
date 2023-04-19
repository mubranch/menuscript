from menu import MenuBarApp
from controller import load_items, open_url, disable
import resources.data.settings as settings
import os


def main():
    settings.init()

    if settings.first_start:
        open_url()
        disable()

    menu = MenuBarApp(
        name="MenuScript",
        icon=os.path.join(settings.image_path, "light.icns"),
        items=load_items(),
    )
    menu.run(debug=True)


if __name__ == "__main__":
    main()
