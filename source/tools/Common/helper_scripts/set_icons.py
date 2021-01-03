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
    launcherPath = data["CurPath"] / (common.formatFileName(data["GameName"]) + platExt)
    launcherFallbackPath = data["CurPath"] / ("BGArmor" + platExt)
    enginePath = data["EngineExecutable"]
    
    if not launcherPath.exists():
        launcherPath = launcherFallbackPath
    
    if launcherPath.exists():
        command = '?./source/tools/Windows/rcedit.exe? --set-icon ?./source/icons/icon-launcher.ico? '
        command += '?' + launcherPath.as_posix() + '?'
        command = command.replace('?', data["Quote"])
        print("\n> Setting icon of launcher...")
        print("Command:", command)
        subprocess.call(command)
        
    if enginePath.exists():
        command = '?./source/tools/Windows/rcedit.exe? --set-icon ?./source/icons/icon-engine.ico? '
        command += '?' + enginePath.as_posix() + '?'
        command = command.replace('?', data["Quote"])
        print("\n> Setting icon of engine...")
        print("Command:", command)
        subprocess.call(command)
        
