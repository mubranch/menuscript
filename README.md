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

<p align="center"> Run essential Python scripts from the macOS menubar with MenuScript.
    <br> 
</p>

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Editing Scripts](#editing_scripts)

## About <a name = "about"></a>

MenuScript is a Python project that uses rumps, a library for creating macOS status bar apps, to run any Python script from the menubar. It provides a convenient way to execute commonly used scripts without needing to open the terminal. If your script requires a virtual environment, you can specify the path to the virtual environment in the config file and then run the script as if it were within the virtual environment. While this project is a personal passion project, it aims to provide a useful tool for streamlining script execution in macOS.

![](https://raw.githubusercontent.com/mubranch/menuscript/master/demo/demo.gif)

## Getting Started <a name = "getting_started"></a>

To install and use MenuScript on macOS, follow these steps:

1. Go to the releases page of the MenuScript project and download the latest release.
2. Move the downloaded release to your Applications folder.
3. Run MenuScript as you would any other macOS application.

If you encounter issues with scripts failing to run, ensure that MenuScript has the necessary permissions. You can grant these permissions by going to System Preferences -> Security & Privacy -> Privacy -> Accessibility, and adding MenuScript to the list of applications allowed to control your computer.

## Editing Scripts <a name = "editing_scripts"></a>

To edit scripts in MenuScript, open the application and click the 'Edit Scripts' button. This will open the config file in your default text editor. You can add new scripts by adding a new line in the following format:

```
(name)[AnythingYouWant](script)(Absolute/path/to/script.py)(venv)(Absolute/path/to/venv/bin/pythonexecutable)
```
Save the config file and restart MenuScript.

The virtual environment (venv) parameter is optional. If you don't want to use a virtual environment, leave it blank and the script
will be executed by your global python installation:

```
(name)[AnythingYouWant](script)(Absolute/path/to/script.py)(venv)[]
```

Periodic updates are made to MenuScript to add new features and improve user-friendliness.

## Add MenuScript to Login Items

To add MenuScript to your login items, follow these steps:

1. Open System Preferences.
2. Click Users & Groups.
3. Click Login Items.
4. Click the '+' button.
5. Navigate to the MenuScript application in your Applications folder and click 'Add'.

## Prerequisites

1. Python 3 must be installed on your macOS system.
2. The application is designed to work specifically on macOS.

## Installing

To install MenuScript on macOS, follow these steps:

1. Download the latest release from the releases page of the MenuScript project.
2. Move the downloaded application to your Applications folder.
3. Run the application. If you want MenuScript to automatically run on startup, you can add it to your login items in System Preferences -> Users & Groups -> Login Items.

## Planned Features
Upcoming Release: Version X.Y.Z

1. GUI for script editing
2. Compatibility with other dependency managers
3. Update checker for easy software updates

## Built Using <a name = "built_using"></a>

- [Rumps](https://rumps.readthedocs.io/en/latest/) - rumps
- [Py2App](https://py2app.readthedocs.io/en/latest/) - Py2App

## Authors <a name = "authors"></a>

- [@mubranch](https://github.com/mubranch) - Idea & Initial work

See also the list of [contributors](https://github.com/mubranch/menuscript/contributors) who participated in this project.

