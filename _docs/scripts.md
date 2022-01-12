---
title: Utility Scripts
description: 
---

# Utility Scripts
The utility scripts are batch/shell scripts that automate some common tasks related to 
BGArmor, such as creating the encrypted `data.dat` file and setting executable icons. 
Some scripts just invoke a Python script, so most of them will need the Python executable 
set at `launcher/xxx/python_executable.txt` in order to run. Below there are some descriptions 
about these scripts provided by BGArmor.

## win-build-data.bat / lin-build-data.sh
This script will build an encrypted `data.dat` file using the `data` folder contents as source.

## win-build-release.bat / lin-build-release.sh
This script will generate releases for the available engine versions provided. With this script:
- You can build the `data.dat` file before building the release.
- You can select the wanted targets (or all) as release targets.
- You can compress all the release targets.

**Note:** Targets will only be available if the respective paths on `launcher` folder are set correctly.

## win-set-icons.bat
This script will set the BGArmor's launcher and blenderplayer executable icons using the 
source files provided at `source/icons`. This script is only available for Windows due to 
Linux not supporting embedded icons in executables.

## win-build-launcher.bat / lin-build-launcher.sh
This script will build the launcher executable from `source/Launcher.c` source file using 
the GCC compiler. You need to install the GCC compiler in order to run this script.

**Note:** This script is not available in release versions of BGArmor, only in the source repository.

## win-minify-launcher.bat / lin-minify-launcher.sh
This script will minify and obfuscate the launcher script at `source/launcher.py` to 
`launcher/launcher.py` using the thirdy party [pyminifier](https://pypi.org/project/pyminifier/) module.

**Note:** This script is not available in release versions of BGArmor, only in the source repository.