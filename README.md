<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://raw.githubusercontent.com/mubranch/menuscript/master/menuscript/resources/imgs/icon.png" alt="Project logo"></a>
</p>

<h3 align="center">MenuScript</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Execute your must have python scripts from the menubar.
    <br> 
</p>

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Built Using](#built_using)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## About <a name = "about"></a>

MenuScript is a Python project that uses rumps, a library for creating macOS status bar apps, to run any Python script from the menubar. It provides a convenient way to execute commonly used scripts without needing to open the terminal. If your script requires a virtual environment, you can specify the path to the virtual environment in the config file and then run the script as if it were within the virtual environment. While this project is a personal passion project, it aims to provide a useful tool for streamlining script execution in macOS.

## Getting Started <a name = "getting_started"></a>

To install and use MenuScript on macOS, follow these steps:

1. Go to the releases folder of the MenuScript project and download the latest release.
2. Move the downloaded release to your Applications folder.
3. Run MenuScript as you would any other macOS application.

If you encounter issues with scripts failing to run, ensure that MenuScript has the necessary permissions. You can grant these permissions by going to System Preferences -> Security & Privacy -> Privacy -> Accessibility, and adding MenuScript to the list of applications allowed to control your computer.

To edit scripts in MenuScript, open the application and click the 'Edit Scripts' button. This will open the config file in your default text editor. You can add new scripts by adding a new line in the following format:

```
(name)[Anything] (script)[Absolute path to script] (venv)[Absolute path to virtual environment python executable]
```
Save the config file and restart MenuScript.

The virtual environment (venv) parameter is optional. If you don't want to use a virtual environment, leave it blank as follows:

```
(name)[Anything] (script)[User/name/path/to/scripty.py] (venv)[]
```

Periodic updates are made to MenuScript to add new features and improve user-friendliness.

### Prerequisites

1. Python 3 must be installed on your macOS system.
2. The application is designed to work specifically on macOS.

### Installing

To install MenuScript on macOS, follow these steps:

1. Download the latest release from the releases folder of the MenuScript project.
2. Move the downloaded application to your Applications folder.
3. Run the application. If you want MenuScript to automatically run on startup, you can add it to your login items in System Preferences -> Users & Groups -> Login Items.

## Built Using <a name = "built_using"></a>

- [Rumps](https://rumps.readthedocs.io/en/latest/) - rumps
- [PyInstaller](https://pyinstaller.org/en/stable/) - PyInstaller

## Authors <a name = "authors"></a>

- [@mubranch](https://github.com/mubranch) - Idea & Initial work

See also the list of [contributors](https://github.com/mubranch/menuscript/contributors) who participated in this project.

## Acknowledgements <a name = "acknowledgement"></a>

- Hat tip to anyone whose code was used
- Inspiration
- References
