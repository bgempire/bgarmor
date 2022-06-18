---
title: Structure
description:
---

# Structure
In this page you'll get a description about each directory and main files contained
in BGArmor structure.

## data
This directory is used to store the game source files. While using BGArmor and
its tasks, this `data` folder is assumed as default, and while the main
blend file in the root of this folder is preferable, there are no restrictions
in order to sctructure this directory's content.

After downloading a [BGArmor release](https://github.com/bgempire/bgarmor/releases)
you can delete all files inside `data` directory, as they are only example files.
Paste your game source files instead.

## engine
This directory is used to store the BGE/UPBGE runtime. You can basically copy
and paste the content of Blender/UPBGE installation folder into the specific
platform directory.

### Folder: engine/Windows32 and engine/Windows64
Should contain the engine runtime files for the Windows platform. Some engine
files are not needed in the final release of the game, so you can delete these
files. Below there is a relation of the **required** files for the engine to run
properly on Windows:

```
engine/Windows*/2.*/python/*
engine/Windows*/blenderplayer.exe
engine/Windows*/OpenAL32.dll
engine/Windows*/OpenColorIO.dll
engine/Windows*/SDL2.dll
engine/Windows*/avcodec-57.dll
engine/Windows*/avdevice-57.dll
engine/Windows*/avformat-57.dll
engine/Windows*/avutil-55.dll
engine/Windows*/libsndfile-1.dll
engine/Windows*/pthreadVC2.dll
engine/Windows*/python35.dll
engine/Windows*/swresample-2.dll
engine/Windows*/swscale-4.dll
```

Although all the files inside `engine/Windows*/2.*/python/` directory are
needed, you can safely delete the `engine/Windows*/2.*/python/lib/test/`
directory in order to save some additional megabytes. All other files **can** be
safely deleted (including `engine/Windows*/blender.exe` executable,
`engine/Windows*/2.*/datafiles/` and `engine/Windows*/2.*/scripts/` folders).

## Folder: engine/Linux32 and engine/Linux64
Should contain the engine runtime files for the Linux platform. Some engine
files are not needed in the final release of the game, so you can delete these
files. Below there is a relation of the **required** files for the engine to run
properly on Linux:

```
engine/Linux*/2.*/python/*
engine/Linux*/blenderplayer*
```

Some files and directories can be safely deleted as mentioned on the
[Windows section](#folder-enginewindows32-and-enginewindows64) section above.

## icons
This folder contains engine and launcher executable icons.
Those icons are used by the task **Set Icons** on BGArmor panel's **Tasks** tab.
You can replace those icons with your own icons (just keep the same names and formats).
The executables that gets their icons replaced are the Windows launcher
(at the `launcher` folder) and Windows `engine` executables, both 32 and 64 bits.

```
icon-engine.ico
icon-launcher.ico
```

**Note:** Since Linux does not support embedded icons neither have a standard
regarding icons, in BGArmor this is a Windows-only feature.

## launcher
This directory contains the needed files for the project to run properly, including
project file with configuration and customized launchers.

### File: launcher/launcher.py
Main script file that runs all BGArmor's logic.

### File: launcher/config.json
Contains all settings regarding the project, independent of platform.
Everything inside this file can be edited inside BGArmor panel, so avoid manually editing it.

### Files: launcher/Launcher.exe and launcher/Launcher.exe
Windows and Linux launcher executables, respectively.
The Windows executable may get its icon replace by the task **Set Icons** on BGArmor panel's **Tasks** tab.
