import os
import platform
import subprocess
from pathlib import Path
from ast import literal_eval
from pprint import pprint

import common

data = common.getData()

if data is not None:
    platExt = ".exe" if platform.system() == "Windows" else ""
    launcherPath = data["CurPath"] / (common.formatFileName(data["GameName"]) + platExt)
    
    if platform.system() == "Linux":
        pass # Todo
        
    command = 'gcc -no-pie -o ?' + launcherPath.as_posix() + '? ?./source/Launcher.c?'
    command = command.replace('?', data["Quote"])
    print("\n> Building launcher...")
    print("Command:", command)
    subprocess.call(command)
    
    if platform.system() == "Windows":
        command = '?./source/tools/Windows/rcedit.exe? --set-icon ?./source/icons/icon-launcher.ico? '
        command += '?' + launcherPath.as_posix() + '?'
        command = command.replace('?', data["Quote"])
        print("\n> Setting icon of launcher...")
        print("Command:", command)
        subprocess.call(command)
    