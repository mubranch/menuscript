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

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](../TODO.md)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

MenuScript uses rumps, and python to run any python script from the menubar. If your script needs a virtual environment, you can specify the path to the virtual environment in the config file and then
run the script as if it were in the virtual environment.

This project is really just a passion project that makes it easier for me to run my common scripts without opening the terminal. I hope you find it useful as well.

## 🏁 Getting Started <a name = "getting_started"></a>

Head to the releases folder and download the latest release. Put it in your Applications folder and run it just like you would any other MacOS application. 

If Scripts are failing to run, make sure you given menuscript the correct permissions. You can do this by going to System Preferences -> Security & Privacy -> Privacy -> Accessibility and adding menuscript to the list of applications that can control your computer.

To edit scripts, open the application and click the 'Edit Scripts' button. This will open the config file in your default text editor. You can add scripts by adding a new line with the following format:
```
(name)[Anything] (script)[Absolute path to script] (venv)[Absolute path to virtual environment python executable]
```
hitting save and restarting the application.

The venv is optional. If you don't want to use a virtual environment, just leave it blank like so:

```
(name)[Anything] (script)[User/name/path/to/scripty.py] (venv)[]
```

Updates are made periodically to add more features and make MenuScript more user friendly.

### Prerequisites

Must have python3 installed.
Must be on MacOS.

### Installing

Step 1: Download the latest release from the releases folder.

Step 2: Put the application in your Applications folder.

Step 3: Run the application. If you want menuscript to run on startup, you can add it to your login items in System Preferences -> Users & Groups -> Login Items.

## ⛏️ Built Using <a name = "built_using"></a>

- [Rumps](https://rumps.readthedocs.io/en/latest/) - rumps
- [PyInstaller](https://pyinstaller.org/en/stable/) - PyInstaller

## ✍️ Authors <a name = "authors"></a>

- [@mubranch](https://github.com/mubranch) - Idea & Initial work

See also the list of [contributors](https://github.com/mubranch/menuscript/contributors) who participated in this project.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Hat tip to anyone whose code was used
- Inspiration
- References
