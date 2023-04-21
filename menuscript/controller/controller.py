# scripty/controllers/controllers.py

from resources import settings
import sys
import subprocess
import os
import shutil
import webbrowser

# import logging
# logging.basicConfig(format="%(process)d-%(levelname)s-%(message)s")
# Implement correct logging later


class ScriptItem:
    def __init__(self, name: str, s_path: str, v_path: str) -> None:
        self.name = name
        self.s_path = s_path
        self.v_path = v_path

    def __str__(self) -> str:
        return f"name: {self.name} | s_path: {self.s_path} | v_path: {self.v_path}"

    def __repr__(self) -> str:
        return f"name: {self.name} | s_path: {self.s_path} | v_path: {self.v_path}"

    def to_dict(self) -> dict:
        return {"name": self.name, "s_path": self.s_path, "v_path": self.v_path}


def items_to_dict(items: list[ScriptItem]) -> dict:
    if items is None:
        return None

    d_items = {}
    for item in items:
        d_items[item.name] = item.to_dict()
    return d_items


def create_config():
    """
    Creates a config file in the user home folder if it doesn't exist.
    Copies the default config file from the data folder into the user home folder.
    Copies the get_started script into the user home folder.
    Copies the settings.py file into the user home folder.

    """

    # read default config file from data folder
    with open(f"{settings.data_path}/config.txt", "r") as f:
        lines = f.readlines()

    # create hidden .menuscript folder if it doesn't exist
    os.makedirs(settings.user_data_path)

    # write new config into user home folder
    with open(f"{settings.user_data_path}/config.txt", "x") as f:
        for line in lines:
            if line.startswith("(name)"):
                print(
                    f"Creating default script at {settings.data_path}/menuscript/resources/data/get_started/main.py"  # noqa: E501
                )
                line = f"(name)[Get Started](script)[{settings.user_data_path}/get_started/main.py](venv)[]"  # noqa: E501
            f.write(line)

    # copy get_started script into user home folder
    src = f"{settings.data_path}/get_started"
    dest = f"{settings.user_data_path}/get_started"

    shutil.copytree(src, dest)


def open_config() -> None:
    print(f"Opening config.txt file in {settings.user_data_path} folder.")
    subprocess.Popen(["open", f"{settings.user_data_path}/config.txt"])


def load_items() -> list[ScriptItem]:
    items = []

    if not os.path.exists(f"{settings.user_data_path}/config.txt"):
        print("Creating config.txt file in user home folder.")
        create_config()

    with open(f"{settings.user_data_path}/config.txt", "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        if line.startswith("("):
            start = line.index("[")
            end = line.index("]", start + 1)
            name = line[start + 1 : end]

            line = line[end:]

            start = line.index("[")
            end = line.index("]", start + 1)
            s_path = line[start + 1 : end]

            line = line[end:]

            start = line.index("[")
            end = line.index("]", start + 1)
            v_path = line[start + 1 : end]

            items.append(ScriptItem(name, s_path, v_path))

    if len(items) == 0:
        return None

    return items


def execute(item: dict[ScriptItem], _) -> any:
    """
    Execute the script displayed in the menu bar. If a virtual environement is
    configured in the config.txt file, it will run with the python executable
    within the virtual environment. This has the benefit of not having to install
    dependencies globally.

    :param item: ScriptItem object
    """
    s_path = item["s_path"]
    v_path = item["v_path"]

    # Check if paths in config.txt are valid

    if not os.path.exists(s_path):
        print(f" '{os.getcwd()}' is the current working directory")
        print(f" '(script)[{s_path}]' in user config file is an invalid file path.")
        return

    if not os.path.exists(v_path):
        if v_path.lower() == "none" or "" or " ":
            v_path = None
        else:
            print(f" '{os.getcwd()}' is the current working directory")
            print(f" '(venv)[{v_path}]' in user config file is an invalid file path.")

    # Get working directory for user's main.py file

    s_name = s_path.split("/")[-1]
    path = "/".join(s_path.split("/")[:-1])
    print(f"Script path: {s_path}")
    print(f"Virtual environment path: {v_path}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Path: {path}")

    if v_path:
        try:
            print(f"Running {s_name}...")
            subprocess.run([v_path, s_name], cwd=path)
            return
        except Exception as e:
            print(e)
            return e

    try:
        print(f"Running {s_name}...")
        subprocess.run(["python", s_name], cwd=path)
        return
    except Exception as e:
        print(e)
        return e


def open_url(url: str = "https://www.github.com/mubranch") -> None:
    """
    Open the Documentation for this project in the user's default browser.
    """
    print(f"Opening {url} in default browser.")
    webbrowser.open(url)


def reset() -> None:
    """
    Remove script and config files from user home folder.
    """
    print("Removing script and config files from user home folder.")
    print("Restarting MenuScript...")
    shutil.rmtree(settings.user_data_path)
    restart()


def restart() -> None:
    """
    Restart MenuScript.
    """

    print("Restarting MenuScript...")

    os.execl(
        sys.executable, os.path.abspath(__file__), *sys.argv
    )  # restarts the MenuScript
