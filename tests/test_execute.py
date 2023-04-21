import subprocess
import pathlib
import sys
import pytest


def execute(item: dict, _) -> any:
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


def test1():
    with pytest.raises(ValueError):
        item = {
            "name": "test",
            "s_path": "/home/runner/work/menuscript/menuscript/tests/test_execute.py",
            "v_path": "None",
        }

        execute(item, None)
