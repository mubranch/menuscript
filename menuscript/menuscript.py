#!/menuscript/menuscript.py

from menu.menu import MenuBarApp
import controller.controller as controller
from resources import paths
import pathlib
import logger.logger as logger
from logger.logger import _log



def main():
    paths.init()
    
    if not paths.user_data_path.exists():
        controller._create_user_data()
    
    logger.init()
        
    items = controller.load_items()

    menu = MenuBarApp(
        name="MenuScript",
        icon=str(pathlib.Path(f"{paths.image_path}/light.icns")),
        items=items,
    )
    
    _log.info("MenuScript started")
    menu.run()



if __name__ == "__main__":
    main()
