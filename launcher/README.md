# BGArmor

## Directory: launcher

This directory contains the needed files for BGArmor to run properly.

## File: launcher.py

Main script file that runs all BGArmor's logic. The file 
`./launcher/launcher.py` is a minified version of `./source/launcher.py`, 
and any of these files will work the same (although the release version of 
BGArmor only contains the minified version).

## File: metadata.dat

Contains the encrypted password to decompress `./data.dat`. It is 
automatically generated at game start as long as the file 
`./source/metadata.txt` exists.

## File: config.json

Contains settings regarding the general release, independent of platform.

- `"GameName"`: String containing the game name. Affects created releases and 
    runtime directories.
- `"MainFile"`: String containing the main blend file name. This is used to 
    run the game with the specified file.
- `"Version"`: String containing the version number of the game. Is used to 
    name releases.
- `"DataFile"`: String containing the relative path to the compressed game 
    data file.
- `"DataSource"`: String containing the relative path to the game source 
    directory. It's used to create the encrypted data file.
- `"Persistent"`: List containing strings with file name patterns. Files that 
    match these patterns will be kept after the launcher is finished. Use 
    this to keep save games and settings of your game.

## File: */python_executable.txt

Contains Python executable path for the specified platform. The path is 
relative to BGArmor's root folder and should point to `./engine/*` in some 
way. This path is important because BGArmor's `launcher.py` will run based on 
this information.

## File: */engine_executable.txt

Contains engine executable path for the specified platform. The path is 
relative to BGArmor's root folder and should point to `./engine/*` in some 
way. This path is important because BGArmor's `launcher.py` will run the 
engine based on this information.