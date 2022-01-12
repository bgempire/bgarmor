---
title: Quickstart Guide
description: 
---

# Quickstart Guide
This guide will help you to quickly setup BGArmor into your BGE/UPBGE project without much hassle. 
There's also a [video](https://www.youtube.com/watch?v=09FAA7xKrok) which presents the main features 
of BGArmor.

## Download the latest release
In order to use BGArmor, download the latest release of BGArmor from the 
[releases page](https://github.com/bgempire/bgarmor/releases). This release already contains the 
launcher executables for both Windows and Linux and the needed directory structure for the development 
pipeline. Extract this archive somewhere and rename its directory to any name you want. You may also 
want to rename the `BGArmor` launcher executable (recommended: use your game name).

## Copy the needed files to BGArmor's directory
Once you have the BGArmor's release extracted in a directory you need two main contents into this 
directory: the game data into the `data` directory and the engine runtimes at `engine` directory.

### Game data
First delete all the files from the `data` directory, they are just for example. If you you already 
have an ongoing project or are creating a new project from scratch, all you have to do is ensure that 
all your project files (blends, textures, scripts, sounds and so on) are contained into the `data` 
directory. Your main blend file (the one which your game is supposed to be launched from) is supposed 
to be at the root directory of `data` and named according to your game's name (because this file name 
will be shown at the runtime's titlebar).

### Engine runtimes
Copy the engine runtimes to the respective directories at `engine`, that is, the BGE / UPBGE's Windows 
executable files to `engine/Windows32` / `engine/Windows64` and respectively the same for the Linux executable files. You can 
actually copy all the contents of the Blender/UPBGE directory, but the `blender` executable and the 
directories `datafiles` and `scripts` from `engine/xxx/2.xx/` directory can be safely deleted.

## Setup the paths
Once all the runtime files and game data were correctly put into their directories, you just need to 
point to them on the configuration text files.

### File: launcher/config.json
This file contains global game information valid for both Windows and Linux releases, such as main blend 
file name, which files are persistent at runtime, game version, etc. Change all the fields to fit your 
game's needs.

**Note:** Keep in mind that `DataFile` and `DataSource` are relative paths from BGArmor's root folder.

```json
{
    "GameName" : "Example Game",
    "Version" : "0.0.2",
    "MainFile" : "Example Game.blend",
    "DataFile" : "./data.dat",
    "DataSource" : "./data",
    "Persistent" : [
        "*.bgeconf",
        "*.sav",
    ]
}
```

### File: launcher/xxx/engine_executable.txt
This file is platform specific because it points to the `blenderplayer` executable. This is needed for the 
BGArmor's launcher executable to be able to run the game and for utility scripts be able to find the runtime 
for other tasks (such as icon changing).

**Notes:** Keep the correct path standard for Windows and Linux (double quotes and single quotes, respectively). 
Keep in mind that `ENGINE_EXECUTABLE` is a relative path from BGArmor's root folder.

```python
ENGINE_EXECUTABLE="./engine/Windows32/blenderplayer.exe"
ENGINE_EXECUTABLE="./engine/Windows64/blenderplayer.exe"
ENGINE_EXECUTABLE='./engine/Linux32/blenderplayer'
ENGINE_EXECUTABLE='./engine/Linux64/blenderplayer'
```

### File: launcher/xxx/python_executable.txt
This file is platform specific because it points to the `python` executable of the engine. This is needed for the 
BGArmor's launcher executable to be able to run the game and for most of the utility shell scripts to run, because 
they actually run Python scripts.

**Notes:** Keep the correct path standard for Windows and Linux (double quotes and single quotes, respectively). 
Keep in mind that `PYTHON_EXECUTABLE` is a relative path from BGArmor's root folder.

```python
PYTHON_EXECUTABLE="./engine/Windows32/2.79/python/bin/python.exe"
PYTHON_EXECUTABLE="./engine/Windows64/2.79/python/bin/python.exe"
PYTHON_EXECUTABLE='./engine/Linux32/2.79/python/bin/python3.5m'
PYTHON_EXECUTABLE='./engine/Linux64/2.79/python/bin/python3.5m'
```

## Create a data.dat file and test run the launcher
To test if the environment is correctly set up, try to create a `data.dat` file by running the shell script 
`xxx-build-data.xxx` (name and extension varies if you're in Windows or Linux). If a new `data.dat` shows up 
in the root directory after running the shell script, the Python path has been correctly set up and you can 
run any other shell script without problems. Once the `data.dat` file is present, you may try to run the 
BGArmor's launcher. If the game launches correctly, everything has been set up correctly. If anything do not 
work as expected, review the settings regarding executable paths as explained above.

**Note:** In Linux you may need to add the execution permission to all the shell scripts and related executables 
mentioned above.

## Releasing the game
Once everything mentioned above is correctly set up you can proceed with the game development normally at the 
`data` directory. Once you are ready to release the game to a specific platform, you only need to run 
`xxx-build-release.xxx` (name and extension varies if you're in Windows or Linux) and follow the instructions 
shown. This script will generate automatically the selected releases on the `release` directory.

If you need an example of how the release file structure looks, take a look at an 
[example game release](https://github.com/bgempire/bgarmor/releases).