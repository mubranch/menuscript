# menuscript/resources/settings.py
import pathlib

def init():
    
    global app_path
    app_path = pathlib.Path(__file__).parent.resolve()
    global data_path
    data_path = pathlib.Path(app_path.joinpath("data"))
    global user_data_path
    user_data_path = pathlib.Path("~").expanduser().joinpath(".menuscript")
    global image_path
    image_path = pathlib.Path(app_path.joinpath("imgs"))
