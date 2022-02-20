from pathlib import Path as _Path
import common as _common


args = _common.getArgs()
data = _common.getProjectData()


def main():
    # type: () -> None
    
    import platform
    import subprocess
    
    print("Started launcher and engine icons setting")
    
    if data:
        
        if args.get("--resource-hacker"):
        
            if platform.system() == "Windows":
                launcherPath = data["CurPath"] / "launcher/Launcher.exe"  # type: _Path
                enginePaths = data["EngineExecutables"]  # type: list[_Path]
                
                if launcherPath.exists():
                    launcherIconPath = data["CurPath"] / "icons/icon-launcher.ico"  # type: _Path
                    command = _getResourceHackerCommand(launcherPath, launcherIconPath)
                    print("\n> Setting icon of launcher...")
                    print("Command:", command)
                    subprocess.call(command)
                    
                else:
                    print("\nX Launcher executable not found! Try using the name", _common.formatFileName(data["GameName"]) + ".exe")
                    
                for enginePath in enginePaths:
                    
                    if "Windows" in enginePath.parent.name:
                        engineIconPath = data["CurPath"] / "icons/icon-engine.ico"  # type: _Path
                        command = _getResourceHackerCommand(enginePath, engineIconPath)
                        print("\n> Setting icon of engine...")
                        print("Command:", command)
                        subprocess.call(command)
                        
            else:
                print("X Command only available on Windows")
            
        else:
            print("X Argument --resource-hacker must be provided")


def _getResourceHackerCommand(executablePath, iconPath):
    # type: (_Path, _Path) -> str
    
    resourceHackerPath = _Path(args.get("--resource-hacker"))
    
    if resourceHackerPath.exists():
        resourceHackerPath = resourceHackerPath.resolve()
    
    command = '?' + resourceHackerPath.as_posix() + '? '
    command += '-open ?' + executablePath.as_posix() + '? '
    command += '-save ?' + executablePath.as_posix() + '? '
    command += '-action addoverwrite -res ?' + iconPath.as_posix() + '? '
    command += '-mask ICONGROUP,APPICON,'
    command = command.replace('?', data["Quote"])
    
    return command


main()