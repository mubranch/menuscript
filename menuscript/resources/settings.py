# scripty/settings.py


def init():
    import os

    global data_path
    data_path = os.path.dirname(__file__) + "/data"
    global user_data_path
    user_data_path = os.path.expanduser("~") + "/.menuscript"
    global image_path
    image_path = data_path.split("data")[0] + "imgs"
    global app_path
    app_path = data_path.split("data")[0][:-1]
