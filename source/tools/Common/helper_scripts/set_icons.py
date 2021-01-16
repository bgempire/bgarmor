import os
import platform
import subprocess
from pathlib import Path
from ast import literal_eval
from pprint import pprint

import common

data = common.getData()

if data is not None:
    
    if platform.system() == "Windows":
        launcherPath = data["CurPath"] / (common.formatFileName(data["GameName"]) + ".exe")
        launcherFallbackPath = [f for f in data["CurPath"].iterdir() if f.name.endswith(".exe") and f.is_file()]
        launcherFallbackPath = launcherFallbackPath[0] if len(launcherFallbackPath) > 0 else data["CurPath"] / ("BGArmor.exe")
        enginePaths = data["EngineExecutables"]
        
        if not launcherPath.exists():
            launcherPath = launcherFallbackPath
        
        if launcherPath.exists():
            command = '?./source/tools/Windows/rcedit.exe? --set-icon ?./source/icons/icon-launcher.ico? '
            command += '?' + launcherPath.as_posix() + '?'
            command = command.replace('?', data["Quote"])
            print("\n> Setting icon of launcher...")
            print("Command:", command)
            subprocess.call(command)
            
        else:
            print("\nX Launcher executable not found! Try using the name", data["GameName"] + ".exe")
            
        for enginePath in enginePaths:
            if "Windows" in enginePath.parent.name:
                command = '?./source/tools/Windows/rcedit.exe? --set-icon ?./source/icons/icon-engine.ico? '
                command += '?' + enginePath.as_posix() + '?'
                command = command.replace('?', data["Quote"])
                print("\n> Setting icon of engine...")
                print("Command:", command)
                subprocess.call(command)
                
    else:
        print("X Script only available on Windows!")
        
