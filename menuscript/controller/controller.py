# scripty/controllers/controllers.py

from resources import settings
import sys
import subprocess
import os
import shutil
import webbrowser
import pathlib

# import logging
# logging.basicConfig(format="%(process)d-%(levelname)s-%(message)s")
# Implement correct logging later


class ScriptItem:
    """
    Represents a script item in the menu bar app.

    :param name: name of the script
    :param s_path: path to the script file
    :param v_path: path to the virtual environment executable

    """

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
    """
    Converts a list of ScriptItem objects to a dictionary.

    :param items: list of ScriptItem objects
    """

    if items is None:
        return None

    d_items = {}
    for item in items:
        d_items[item.name] = item.to_dict()

    return d_items


def create_config() -> None:
    """
    Updates the config file in the user's home folder if it exists; otherwise, creates a
    new one. Copies the default config file from the data folder into the user's home
    folder. Also, copies the get_started script file into the user's home folder.
    """

    if pathlib.Path(f"{settings.user_data_path}/config.txt").exists():
        raise FileExistsError("User config file already exists but should not.")

    # read default config file from data folder
    with open(f"{settings.data_path}/config.txt", "r") as f:
        lines = f.readlines()

    # create hidden .menuscript folder if it doesn't exist
    pathlib.Path.mkdir(settings.user_data_path)

    try:
        # write new config into user home folder
        with open(f"{settings.user_data_path}/config.txt", "x") as f:
            for line in lines:
                if line.startswith("(name)"):
                    line = f"(name)[Get Started](script)[{settings.user_data_path}/get_started/main.py](venv)[]"  # noqa: E501
                f.write(line)

    except PermissionError:
        raise PermissionError(
            "MenuScript does not have permission to write to the user home directory."
        )

    # copy get_started script into user home folder
    src = f"{settings.data_path}/get_started"
    dest = f"{settings.user_data_path}/get_started"

    shutil.copytree(src, dest)


def open_config() -> None:
    """
    Opens the config file in the user's config file with the default text editor.
    """
    subprocess.Popen(["open", f"{settings.user_data_path}/config.txt"])


def load_items() -> any:
    """
    Loads the items from the config file in the user's home folder. Returns a list of
    ScriptItem objects.
    """
    items = []

    if not pathlib.Path(f"{settings.user_data_path}/config.txt").exists():
        create_config()

    with open(f"{settings.user_data_path}/config.txt", "r") as f:
        lines = f.readlines()

    # format config file line to get name, script path, and virtual environment path

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

            if name == "" or s_path == "":
                raise ValueError(
                    "One of the items in the user config file is missing a value."
                )

            items.append(ScriptItem(name, s_path, v_path))

    if len(items) == 0:
        return None

    return items


def execute(item: dict[ScriptItem], _) -> any:
    """
    Execute the script displayed in the menu bar. If a virtual environement is
    configured in the config.txt file, it will activate the virtual environemnt.
    Then run the script.

    :param item: ScriptItem object
    """

    s_path = item["s_path"]
    s_path = pathlib.Path(s_path)
    v_path = item["v_path"]
    v_path = pathlib.Path(v_path)

    # Check if paths in config.txt are valid

    if not s_path.is_file() or not str(s_path).endswith(".py"):
        raise ValueError(
            "...(script)[path/to/script]... in user config file is not a '.py' file"
        )

    if not v_path.is_file():
        if str(v_path).lower() == "none" or "." or " ":
            v_path = None

    # Get script name from s_path
    s_name = str(s_path).split("/")[-1]
    path = pathlib.Path("/".join(str(s_path).split("/")[:-1]))

    if v_path:  # will be None or a PoxisPath object
        venv_activate = str(v_path).split("bin")[0] + "bin/activate"
        cmd = f"source {venv_activate}; {v_path} {s_name}"  # Set bash command for Popen

        try:
            p = subprocess.Popen(cmd, cwd=str(path), stdout=subprocess.PIPE, shell=True)
            print(p.communicate()[0])
            return
        except Exception as e:
            return e

    # If no virtual environment is configured, run script with global python interpreter
    try:
        subprocess.run([str(pathlib.Path(sys.executable)), s_name], cwd=path)
        return
    except Exception as e:
        return e


def open_url(url: str = "https://www.github.com/mubranch") -> None:
    """
    Open the Documentation for this project in the user's default browser.
    """

    webbrowser.open(url)


def reset() -> None:
    """
    Remove script and config files from user home folder.
    """

    shutil.rmtree(settings.user_data_path)


def restart(self) -> None:
    """
    Restart MenuScript.
    """

    os.execl(
        sys.executable, os.path.abspath(__file__), *sys.argv
    )  # restarts the MenuScript
