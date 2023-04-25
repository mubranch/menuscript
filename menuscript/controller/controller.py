# menuscript/controllers/controllers.py

from resources import settings
import rumps
import sys
import subprocess
import os
import shutil
import webbrowser
import pathlib
import logging


class _notify_error: # type: ignore
    def __init__(self, message):
        self = rumps.notification("MenuScript", "Error", message, icon=str(pathlib.Path(f"{settings.image_path}/icon.icns")))
 
 
class _notify_info: # type: ignore
    def __init__(self, message):
        self = rumps.notification("MenuScript", "Alert", message, icon=str(pathlib.Path(f"{settings.image_path}/icon.icns")))  


def _create_user_data() -> None:
    """
    Updates the config file in the user's home folder if it exists; otherwise, creates a
    new one. Copies the default config file from the data folder into the user's home
    folder. Also, copies the example script file into the user's home folder.
    """
    
    try:
        pathlib.Path.mkdir(pathlib.Path(f"{settings.user_data_path}"), exist_ok=False)
    except Exception as e:
        logging.info(f"User data already exists at {settings.user_data_path}")
        
    # read default config file from data folder
    try: 
        with open(f"{settings.data_path}/config.txt", "r") as f:
            lines = f.readlines()
            
    except Exception as e:
        logging.error(f"Failed to read config with error: '{str(e)}'")
        return

    try:
        # write new config into user home folder
        with open(f"{settings.user_data_path}/.config.txt", "x") as f:
            for line in lines:
                if line.startswith("(name)"):
                    line = f"(name)[Example](source)[{settings.user_data_path}/example/main.py](interpreter)[]\n"
                f.write(line)

    except Exception as e:
        logging.error(f"Failed to write config with error: '{str(e)}'")
        _notify_error(f"Failed to write config with error: '{str(e)}'")

    # copy example script into user home folder
    src = f"{settings.data_path}/example"
    dest = f"{settings.user_data_path}/example"

    shutil.copytree(src, dest)

    # copy user data into user home folder
    src = str(pathlib.Path(f"{settings.data_path}/.data.txt"))
    dest = f"{settings.user_data_path}/.data.txt"

    shutil.copyfile(src, dest)

    _copy_over_ui()
    logging.info(f"User data created at {settings.user_data_path}")


def _copy_over_ui() -> None:
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
    else:
        logging.error("User data folder does not exist.")


def load_items() -> list:
    """
    Loads the items from the config file in the user's home folder. Returns a list of
    ScriptItem objects.
    """

    try:
        with open(f"{settings.user_data_path}/.config.txt", "r") as f:
            lines = f.readlines()
    except Exception as e:
        logging.error(f"Failed to read config with error: '{str(e)}'")
        _notify_error(f"Failed to read config with error: '{str(e)}'")
        logging.error("Exiting with error code 1")
        exit(1)

    # format config file line to get name, script path, and virtual environment path

    items = _config_to_items(lines)

    if len(items) == 0:
        return []

    logging.info(f"Returning {len(items)} items from config file.")
    return items

def _config_to_items(lines: list) -> list:
    items = []
    names = set()
    
    for i, line in enumerate(lines):
        
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
                logging.error("Invalid config file - scripts must have a name.")
                rumps.notification(
                    title="MenuScript",
                    subtitle="Invalid config file",
                    message="Scripts must have a name.",
                )
                continue

            if name in names:
                logging.info(f"Repeated script name: '{name}' in line: '{i}'")
                _notify_info(f"Scripts must have unique names. Repeated script name: '{name}' in line: '{i}'")

            if not pathlib.Path(interpreter).is_file():
                interpreter = None

            names.add(name)
            items.append((name, source, interpreter))
            
    return items
    
    

def write_item(item: tuple) -> None:
    """
    Writes a script item to the user_config.txt file.

    """
    try:
        with open(f"{settings.user_data_path}/.config.txt", "a") as f:
            f.write(f"(name)[{item[0]}](source)[{item[1]}](interpreter)[]\n")
    except Exception as e:
        logging.error(f"Could not write item with error: '{str(e)}'")
        return


def remove_item(item: tuple) -> None:
    """
    Removes a script item from the user_config.txt file.

    """
    try:
        with open(f"{settings.user_data_path}/.config.txt", "r") as f:
            lines = f.readlines()
    except Exception as e:
        logging.error(f"Could not open config with error: '{str(e)}'")
        return

    try:
        with open(f"{settings.user_data_path}/.config.txt", "w") as f:
            for line in lines:
                if line.startswith("(name)"):
                    continue
                f.write(line)

    except Exception as e:
        logging.error(f"Could not write to config with error: '{str(e)}'")
        _notify_error(f"Could not write to config with error: '{str(e)}'")
        




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


def open_interpreter_picker():
    command = ["python", f"{settings.user_data_path}/interpreter/main.py"]
    try:
        logging.info(f"Opening file picker at '{settings.user_data_path}' with command: '{command}'")
        p = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        _notify_info(f"New interpreter: {p.communicate()[0].decode('utf-8')}")
        logging.info(f"New interpreter: {p.communicate()[0].decode('utf-8')}")
        return p.communicate()[0].decode("utf-8")
        
    except Exception as e:
        logging.error(f"Failed to open interpreter picker at '{settings.user_data_path}' with error: {str(e)}")
        return


def open_filepicker():
    command = ["python", f"{settings.user_data_path}/file/main.py"]
    try:
        logging.info(f"Opening file picker at '{settings.user_data_path}' with command: '{command}'")
        p = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        _notify_info(f"New source: {p.communicate()[0].decode('utf-8')}")
        logging.info(f"New source: {p.communicate()[0].decode('utf-8')}")
        return p.communicate()[0].decode("utf-8")
    except Exception as e:
        logging.error(f"Failed to open interpreter picker at '{settings.user_data_path}' with error: {str(e)}")
        return


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

    try:
        with open(f"{settings.user_data_path}/.config.txt", "r") as f:
            lines = f.readlines()
    except Exception as e:
        logging.error(f"Could not open config with error: '{str(e)}'")
        return False

    try:
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
    except Exception as e:
        logging.error(f"Could not write to config with error: '{str(e)}'")
        return False


def update_source(item: tuple, new_source: str):
    if new_source == "":
        _notify_error("Script source cannot be empty.")
        logging.error("Script source cannot be empty.")
        return False

    try:
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
    except Exception as e:
        logging.error(f"Could not write to open/write config with error: '{str(e)}'")
        return False


def update_interpreter(item: tuple, new_interpreter: str) -> bool:
    if new_interpreter == "":
        return False

    try:
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
    except Exception as e:
        logging.error(f"Could not write to open/write config with error: '{str(e)}'")
        return False


def get_num_executions():
    
    try:
        with open(f"{settings.user_data_path}/.data.txt", "r") as f:
            lines = f.readlines()

        for line in lines:
            if line.startswith("(executions)"):
                start = line.index(")")
                return int(line[start + 1 :])
            
    except Exception as e:
        logging.error(f"Could not read from data file with error: '{str(e)}'")
        return 0


def increment_execution_count() -> None:
    
    try:
        
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
                
    except Exception as e:
        logging.error(f"Could not read from/write to data file with error: '{str(e)}'")
        return


def execute(item: tuple):
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
        _notify_error("Invalid script source.")
        logging.error("Invalid script source.")

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


def open_config() -> None:
    """
    Opens the config file in the user's config file with the default text editor.
    """
    subprocess.Popen(["open", f"{settings.user_data_path}/.config.txt"])
    
    
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
