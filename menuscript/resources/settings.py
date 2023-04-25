# menuscript/resources/settings.py
import logging
import pathlib
import controller.controller as controller

def init():
    
    global app_path
    app_path = pathlib.Path(__file__).parent.resolve()
    global data_path
    data_path = pathlib.Path(app_path.joinpath( "data"))
    global user_data_path
    user_data_path = pathlib.Path("~").expanduser().joinpath(".menuscript")
    global image_path
    image_path = pathlib.Path(app_path.joinpath( "imgs"))

    try:
        logging.basicConfig(
            filename=user_data_path.joinpath("app.log"), filemode="w", format="%(name)s - %(levelname)s - %(message)s"
        )
    except:
        controller._create_user_data()
        logging.basicConfig(
            filename=user_data_path.joinpath("app.log"), filemode="w", format="%(name)s - %(levelname)s - %(message)s"
        )