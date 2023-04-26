# menuscript/menuscript.py

from menu.menu import MenuBarApp
import controller.controller as controller
from resources import paths
import pathlib
import logger.logger as logger
from logger.logger import _log


def main():
    paths.init()
    
    if not paths.user_data_path.exists():
        controller.create_user_data()
    
    logger.init()
    _log.info("------Initializing MenuScript------")
    
    _log.info(f"App path, '{paths.app_path}'")
    _log.info(f"User data path, '{paths.user_data_path}'")
        
    items = controller.load_items()
    _log.info(f"Items read: {items} from {paths.user_data_path}")

    menu = MenuBarApp(
        name="MenuScript",
        icon=str(pathlib.Path(f"{paths.image_path}/light.icns")),
        items=items,
    )
    
    _log.info("------MenuScript started------")
    menu.run()
    _log.info("------MenuScript closed------")



if __name__ == "__main__":
    main()
