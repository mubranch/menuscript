# scripty/controllers/controllers.py

import resources.data.settings as settings
import subprocess
import os
import shutil
import webbrowser
import logging

logging.basicConfig(format="%(process)d-%(levelname)s-%(message)s")


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
    d_items = {}
    for item in items:
        d_items[item.name] = item.to_dict()
    return d_items


def create_config():
    src = f"{settings.data_path}/config.txt"
    dest = f"{settings.data_path}/user_config.txt"

    shutil.copy(src, dest)


def open_config():
    subprocess.Popen(["open", f"{settings.data_path}/user_config.txt"])


def load_items() -> list[ScriptItem]:
    items = []

    if not os.path.exists(f"{settings.data_path}/user_config.txt"):
        create_config()
        return None

    with open(f"{settings.data_path}/user_config.txt", "r") as f:
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
    configured in the user_config.txt file, it will run with the python executable
    within the virtual environment. This has the benefit of not having to install
    dependencies globally.

    :param item: ScriptItem object
    """
    s_path = item["s_path"]
    v_path = item["v_path"]

    cwd = os.getcwd()

    if s_path.startswith("."):
        s_path = cwd + s_path[1:]

    if v_path.startswith("."):
        v_path = cwd + v_path[1:]

    # Check if paths in user_config.txt are valid

    if not os.path.exists(s_path):
        logging.error(f" '{os.getcwd()}' is the current working directory")
        logging.error(
            f" '(script)[{s_path}]' in user_config.txt is an invalid file path."
        )
        return

    if not os.path.exists(v_path):
        if v_path.lower() == "none" or "" or " ":
            v_path = None
        else:
            logging.error(f" '{os.getcwd()}' is the current working directory")
            logging.error(
                f" '(venv)[{v_path}]' in user_config.txt is an invalid file path."
            )

    # Get working directory for user's main.py file

    s_name = s_path.split("/")[-1]
    path = "/".join(s_path.split("/")[:-1])

    if v_path:
        try:
            subprocess.Popen([v_path, s_name], cwd=path)
            logging.info(f"Running {s_name}...")
            return
        except Exception as e:
            logging.error(e)
            return e

    try:
        subprocess.Popen(["python3", s_name], cwd=path)
        logging.info(f"Running {s_name}...")
        return
    except Exception as e:
        logging.error(e)
        return e


def open_url():
    """
    Open the Documentation for this project in the user's default browser.
    """

    webbrowser.open("https://www.github.com/mubranch")


def disable() -> None:
    with open(f"{settings.data_path}/settings.py", "r") as f:
        lines = f.readlines()

    with open(f"{settings.data_path}/settings.py", "w") as f:
        for line in lines:
            if line.startswith("    first_start ="):
                f.write("    first_start = False")
            else:
                f.write(line)
