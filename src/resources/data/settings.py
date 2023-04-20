# scripty/settings.py


def init():
    import os

    global data_path
    data_path = os.path.dirname(__file__)
    print(data_path)
    global image_path
    image_path = data_path.split("data")[0] + "imgs"
    print(image_path)
    global app_path
    app_path = data_path.split("resources")[0]
    print(app_path)
    global first_start
    first_start = False
