# menuscript/controllers/controllers.py

from resources import settings
import rumps
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
    :param source: path to the script file
    :param interpreter: path to the virtual environment executable

    """

    def __init__(self, name: str, source: str, interpreter: str, *args) -> None:
        self.name = name
        self.source = source
        self.interpreter = interpreter
        self.schedule = args[0] if len(args) > 0 else None

    def __str__(self) -> str:
        return f"name: {self.name} | source: {self.source} | interpreter: {self.interpreter} | schedule: {self.schedule}"

    def __repr__(self) -> str:
        return f"name: {self.name} | source: {self.source} | interpreter: {self.interpreter} | schedule: {self.schedule}"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "source": self.source,
            "interpreter": self.interpreter,
            "schedule": self.schedule,
        }


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


def schedule_job(item: ScriptItem):
    """
        Executes a script item in a cron job.

        :param item: the script item to execute.

    Minute. The minute of the hour the command will run on, ranging from 0-59.
    Hour. The hour the command will run at, ranging from 0-23 in the 24-hour notation.
    Day of the month. The day of the month the user wants the command to run on, ranging from 1-31.
    Month. The month that the user wants the command to run in, ranging from 1-12, thus representing January-December.
    Day of the week. The day of the week for a command to run on, ranging from 0-6, representing Sunday-Saturday. In some systems, the value 7 represents Sunday.

    """

    pass


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
                    line = f"(name)[Get Started](script)[{settings.user_data_path}/get_started/main.py](venv)[]"
                f.write(line)

    except PermissionError:
        rumps.notification(
            title="MenuScript",
            subtitle="Initial setup",
            message="MenuScript does not have permission to write to the user home directory.",
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
    names = set()

    if not pathlib.Path(f"{settings.user_data_path}/config.txt").exists():
        create_config()

    with open(f"{settings.user_data_path}/config.txt", "r") as f:
        lines = f.readlines()

    # format config file line to get name, script path, and virtual environment path

    for line in lines:
        if not line:
            break

        line = line.strip()

        if line.startswith("("):
            start = line.index("[")
            end = line.index("]", start + 1)
            name = line[start + 1 : end]

            line = line[end:]

            start = line.index("[")
            end = line.index("]", start + 1)
            source = line[start + 1 : end]

            line = line[end:]

            start = line.index("[")
            end = line.index("]", start + 1)
            interpreter = line[start + 1 : end]

            if name == "" or not pathlib.Path(source).is_file():
                rumps.notification(
                    title="MenuScript",
                    subtitle="Invalid config file",
                    message="Scripts must have a name, and the script path must be a valid file path.",
                )
                continue

            if name in names:
                rumps.notification(
                    title="MenuScript",
                    subtitle="Invalid config file",
                    message="Scripts must have unique names. This is a limitation of Rumps,"
                    " the framework used to build MenuScript.",
                )

            names.add(name)
            items.append(ScriptItem(name, source, interpreter))

    if len(items) == 0:
        return None

    return items


def update_name(item: dict, new_name: str) -> None:
    """
    Updates the name of a script item in the config file.

    :param item: the script item to update
    :param new_name: the new name of the script item
    """

    if new_name == "":
        rumps.notification(
            title="MenuScript",
            subtitle="Invalid name",
            message="Script names cannot be empty.",
        )
        return

    with open(f"{settings.user_data_path}/config.txt", "r") as f:
        lines = f.readlines()

    with open(f"{settings.user_data_path}/config.txt", "w") as f:
        name = item.get("name")
        source = item.get("source")
        interpreter = item.get("interpreter")
        for line in lines:
            line = line.strip()  # clear whitespace
            if line.startswith(f"(name)[{name}]"):
                line = f"(name)[{new_name}](script)[{source}](venv)[{interpreter}]"
            f.write(f"{line}\n")


def execute(item: dict[ScriptItem], _) -> any:
    """
    Execute the script displayed in the menu bar. If a virtual environement is
    configured in the config.txt file, it will activate the virtual environemnt.
    Then run the script.

    :param item: ScriptItem object
    """

    source = item["source"]
    source = pathlib.Path(source)
    interpreter = item["interpreter"]
    interpreter = pathlib.Path(interpreter)

    # Check if paths in config.txt are valid

    if not source.is_file() or not str(source).endswith(".py"):
        raise ValueError(
            "...(script)[path/to/script]... in user config file is not a '.py' file"
        )

    if not interpreter.is_file():
        if str(interpreter).lower() == "none" or "." or " ":
            interpreter = None

    # Get script name from source
    s_name = str(source).split("/")[-1]
    path = pathlib.Path("/".join(str(source).split("/")[:-1]))

    if interpreter:  # will be None or a PoxisPath object
        venv_activate = str(interpreter).split("bin")[0] + "bin/activate"
        cmd = f"source {venv_activate}; {interpreter} {s_name}"  # Set bash command for Popen

        try:
            p = subprocess.Popen(cmd, cwd=str(path), stdout=subprocess.PIPE, shell=True)
            rumps.notification(
                title="MenuScript",
                subtitle="Running script",
                message=f"Script executed with message {p.communicate()}",
            )
            return
        except Exception as e:
            rumps.notification(title="MenuScript", subtitle="Error", message=e.__str__)
            return e

    # If no virtual environment is configured, run script with global python interpreter
    try:
        p = subprocess.run(
            [str(pathlib.Path(sys.executable)), s_name],
            stdout=subprocess.PIPE,
            cwd=path,
        )

        msg = None

        if p.check_returncode() is None:
            msg = "Success"

        rumps.notification(
            title="MenuScript",
            subtitle="Running script",
            message=f"Script executed with message '{msg}'",
        )
        return
    except Exception as e:
        rumps.notification(title="MenuScript", subtitle="Error", message=e.__str__)
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
    rumps.notification(
        title="MenuScript",
        subtitle="Reset",
        message="Reset complete. Restart MenuScript for changes to take effect",
    )


def restart(self) -> None:
    """
    Restart MenuScript.
    """
    os.execl(
        sys.executable, os.path.abspath(__file__), *sys.argv
    )  # restarts the MenuScript
