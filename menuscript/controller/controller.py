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


def schedule_job(item: dict):
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


def remove_item(item: tuple) -> None:
    """
    Removes a script item from the user_config.txt file.

    """

    with open(f"{settings.user_data_path}/.config.txt", "r") as f:
        lines = f.readlines()

    try:
        with open(f"{settings.user_data_path}/.config.txt", "w") as f:
            for line in lines:
                if line.startswith("(name)"):
                    continue
                f.write(line)

    except PermissionError:
        rumps.notification(
            title="MenuScript",
            subtitle="Initial setup",
            message="MenuScript does not have permission to write to the user home directory.",
        )


def write_item(item: tuple) -> None:
    """
    Writes a script item to the user_config.txt file.

    """

    with open(f"{settings.user_data_path}/.config.txt", "a") as f:
        f.write(f"(name)[{item[0]}](source)[{item[1]}](interpreter)[]\n")


def open_interpreter_picker() -> str:
    command = ["python", f"{settings.user_data_path}/interpreter/main.py"]
    try:
        p = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        rumps.notification(
            title="MenuScript",
            subtitle="Interpreter selected",
            message=f"New interpreter: {get_interpreter_label(p.communicate()[0].decode('utf-8'))}",
        )
        return p.communicate()[0].decode("utf-8")
    except Exception as e:
        raise (e)


def open_filepicker() -> str:
    command = ["python", f"{settings.user_data_path}/file/main.py"]
    try:
        p = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        rumps.notification(
            title="MenuScript",
            subtitle="Source selected",
            message=f"New source: {get_source_label(p.communicate()[0].decode('utf-8'))}",
        )
        return p.communicate()[0].decode("utf-8")
    except Exception as e:
        print(e)
        raise (e)


def move_ui() -> None:
    """
    Copy filedialog UI to user .menuscript folder.

    """
    if pathlib.Path(f"{settings.user_data_path}").exists():
        src = f"{settings.data_path}/file"
        dest = f"{settings.user_data_path}/file"

        shutil.copytree(src, dest)

        src = f"{settings.data_path}/interpreter"
        dest = f"{settings.user_data_path}/interpreter"

        shutil.copytree(src, dest)


def increment_execution_count() -> None:
    with open(f"{settings.user_data_path}/.data.txt", "r") as f:
        lines = f.readlines()

    with open(f"{settings.user_data_path}/.data.txt", "w") as f:
        for line in lines:
            line.strip()
            if line.startswith("(executions)"):
                num = line.index(")")
                string = line[num + 1 :]
                line = f"(executions){int(string)+1}"
            f.write(line)


def create_user_data() -> None:
    """
    Updates the config file in the user's home folder if it exists; otherwise, creates a
    new one. Copies the default config file from the data folder into the user's home
    folder. Also, copies the example script file into the user's home folder.
    """

    if pathlib.Path(f"{settings.user_data_path}/.config.txt").exists():
        raise FileExistsError("User config file already exists but should not.")

    # read default config file from data folder
    with open(f"{settings.data_path}/config.txt", "r") as f:
        lines = f.readlines()

    # create hidden .menuscript folder if it doesn't exist
    pathlib.Path.mkdir(settings.user_data_path)

    try:
        # write new config into user home folder
        with open(f"{settings.user_data_path}/.config.txt", "x") as f:
            for line in lines:
                if line.startswith("(name)"):
                    line = f"(name)[Example](source)[{settings.user_data_path}/example/main.py](interpreter)[]\n"
                f.write(line)

    except PermissionError:
        rumps.notification(
            title="MenuScript",
            subtitle="Initial setup",
            message="MenuScript does not have permission to write to the user home directory.",
        )

    # copy example script into user home folder
    src = f"{settings.data_path}/example"
    dest = f"{settings.user_data_path}/example"

    shutil.copytree(src, dest)

    # copy user data into user home folder
    src = str(pathlib.Path(f"{settings.data_path}/.data.txt"))
    dest = f"{settings.user_data_path}/.data.txt"

    shutil.copyfile(src, dest)

    move_ui()


def open_config() -> None:
    """
    Opens the config file in the user's config file with the default text editor.
    """
    subprocess.Popen(["open", f"{settings.user_data_path}/.config.txt"])


def get_source_label(source: str) -> str:
    s = str(pathlib.Path(source)).split("/")[-1]
    return f"Source: '{s}'"


def get_interpreter_label(interpreter: str) -> str:
    if not interpreter:
        return "Interpreter: 'Global'"
    i_ex_name = str(pathlib.Path(interpreter)).split("/")[-1]
    return f"Interpreter: '(venv) {i_ex_name}'"


def get_name_label(name: str) -> str:
    return f"Name: '{name}'"


def load_items() -> any:
    """
    Loads the items from the config file in the user's home folder. Returns a list of
    ScriptItem objects.
    """
    items = []
    names = set()

    if not pathlib.Path(f"{settings.user_data_path}/.config.txt").exists():
        create_user_data()

    with open(f"{settings.user_data_path}/.config.txt", "r") as f:
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

            if name == "":
                rumps.notification(
                    title="MenuScript",
                    subtitle="Invalid config file",
                    message="Scripts must have a name.",
                )
                continue

            if name in names:
                rumps.notification(
                    title="MenuScript",
                    subtitle="Invalid config file",
                    message="Scripts must have unique names. This is a limitation of Rumps,"
                    " the framework used to build MenuScript.",
                )

            if not pathlib.Path(interpreter).is_file():
                interpreter = None

            names.add(name)
            items.append((name, source, interpreter))

    if len(items) == 0:
        return None

    return items


def update_name(item: tuple, new_name: str) -> bool:
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
        return False

    with open(f"{settings.user_data_path}/.config.txt", "r") as f:
        lines = f.readlines()

    with open(f"{settings.user_data_path}/.config.txt", "w") as f:
        name = item[0]
        source = item[1]
        interpreter = item[2]
        for line in lines:
            line = line.strip()  # clear whitespace
            if line.startswith(f"(name)[{name}]"):
                line = (
                    f"(name)[{new_name}](source)[{source}](interpreter)[{interpreter}]"
                )
            f.write(f"{line}\n")

    return True


def get_num_executions() -> int:
    with open(f"{settings.user_data_path}/.data.txt", "r") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("(executions)"):
            start = line.index(")")
            return int(line[start + 1 :])


def update_source(item: tuple, new_source: str) -> bool:
    if new_source == "":
        rumps.notification(
            title="MenuScript",
            subtitle="Invalid source",
            message="Script source cannot be empty.",
        )
        return False

    with open(f"{settings.user_data_path}/.config.txt", "r") as f:
        lines = f.readlines()

    with open(f"{settings.user_data_path}/.config.txt", "w") as f:
        name = item[0]
        interpreter = item[2]
        for line in lines:
            line = line.strip()  # clear whitespace
            if line.startswith(f"(name)[{name}]"):
                line = (
                    f"(name)[{name}](source)[{new_source}](interpreter)[{interpreter}]"
                )
            f.write(f"{line}\n")

    return True


def update_interpreter(item: tuple, new_interpreter: str) -> bool:
    if new_interpreter == "":
        rumps.notification(
            title="MenuScript",
            subtitle="Invalid source",
            message="Script source cannot be empty.",
        )
        return False

    with open(f"{settings.user_data_path}/.config.txt", "r") as f:
        lines = f.readlines()

    with open(f"{settings.user_data_path}/.config.txt", "w") as f:
        name = item[0]
        source = item[1]
        for line in lines:
            line = line.strip()  # clear whitespace
            if line.startswith(f"(name)[{name}]"):
                line = (
                    f"(name)[{name}](source)[{source}](interpreter)[{new_interpreter}]"
                )
            f.write(f"{line}\n")

    return True


def execute(item: tuple) -> any:
    """
    Execute the script displayed in the menu bar. If a virtual environement is
    configured in the config.txt file, it will activate the virtual environemnt.
    Then run the script.

    :param item: ScriptItem object
    """

    source = item[1]
    source = pathlib.Path(source)
    interpreter = item[2]

    try:
        interpreter = pathlib.Path(interpreter)
    except TypeError:
        interpreter = None

    # Check if paths in config.txt are valid
    if not source.is_file() or not str(source).endswith(".py"):
        raise ValueError(
            "...(script)[path/to/script]... in user config file is not a '.py' file"
        )

    if interpreter is not None:
        if (
            str(interpreter).lower() == "none"
            or str(interpreter).lower() == "."
            or str(interpreter).lower() == " "
        ):
            interpreter = None

    # Get script name from source
    s_name = str(source).split("/")[-1]
    path = pathlib.Path("/".join(str(source).split("/")[:-1]))

    if interpreter:  # will be None or a PoxisPath object
        venv_activate = str(interpreter).split("bin")[0] + "bin/activate"
        cmd = [
            f"source {venv_activate}",
            f"{interpreter} {s_name}",
        ]  # Set bash command for Popen

        try:
            p = subprocess.Popen(
                cmd,
                cwd=str(path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )
            rumps.notification(
                title="MenuScript",
                subtitle="Running script",
                message=f"Script executed with message {p.communicate()[0].decode('utf-8')}",
            )
            increment_execution_count()
            return
        except Exception as e:
            rumps.notification(title="MenuScript", subtitle="Error", message=e.__str__)
            return e

    # If no virtual environment is configured, run script with global python interpreter
    try:
        cmd = [str(pathlib.Path(sys.executable)), s_name]
        p = subprocess.Popen(
            cmd,
            cwd=str(path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        rumps.notification(
            title="MenuScript",
            subtitle="Running script",
            message=f"Script executed with message {p.communicate()[0].decode('utf-8')}",
        )
        increment_execution_count()
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
