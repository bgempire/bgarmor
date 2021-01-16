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
    launcherPath = data["CurPath"] / ("BGArmor" + platExt)
    
    print("\n> Building launcher...")
    
    if platform.system() == "Linux":
        command = 'gcc -m32 -no-pie -c ./source/Launcher.c -o Launcher.o'
        print("Command:", command)
        os.system(command)
        command = "gcc -m32 -no-pie -o ?" + launcherPath.as_posix() + "? Launcher.o"
        command = command.replace('?', data["Quote"])
        print("Command:", command)
        os.system(command)
    
    if platform.system() == "Windows":
        command = 'gcc -m32 -no-pie -o ?' + launcherPath.as_posix() + '? ?./source/Launcher.c?'
        command = command.replace('?', data["Quote"])
        print("Command:", command)
        subprocess.call(command)
        
        command = '?./source/tools/Windows/ResourceHacker.exe? '
        command += '-open ?' + launcherPath.as_posix() + '? '
        command += '-save ?' + launcherPath.as_posix() + '? '
        command += '-action addoverwrite -res ?./source/icons/icon-launcher.ico? '
        command += '-mask ICONGROUP,APPICON, '
        command = command.replace('?', data["Quote"])
        print("\n> Setting icon of launcher...")
        print("Command:", command)
        subprocess.call(command)
    
