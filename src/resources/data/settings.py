# scripty/settings.py


def init():
    import os

    global data_path
    data_path = os.path.dirname(__file__)
    global image_path
    image_path = data_path.split("src")[0] + "src/resources/imgs"
    global app_path
    app_path = data_path.split("data")[0]
    global first_start
    first_start = False