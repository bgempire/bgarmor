from pathlib import Path as _Path
import common as _common
import platform


args = _common.getArgs()
data = _common.getProjectData()


def main():
    # type: () -> None

    import platform
    import subprocess

    print("Started launcher and engine icons setting")

    if data:

        if args.get("--resource-hacker"):

            launcherPath = data["CurPath"] / "launcher/Launcher.exe"  # type: _Path
            enginePaths = data["EngineExecutables"]  # type: dict[str, _Path]

            if launcherPath.exists():
                launcherIconPath = data["CurPath"] / "icons/icon-launcher.ico"  # type: _Path
                command = _getResourceHackerCommand(launcherPath, launcherIconPath)
                print("\n> Setting icon of launcher...")
                print("Command:", " ".join(command))
                subprocess.call(command)

            else:
                print("\nX Launcher executable not found! Try using the name", _common.formatFileName(data["GameName"]) + ".exe")

            for enginePath in enginePaths.values():

                if "Windows" in enginePath.parent.name:
                    engineIconPath = data["CurPath"] / "icons/icon-engine.ico"  # type: _Path
                    command = _getResourceHackerCommand(enginePath, engineIconPath)
                    print("\n> Setting icon of engine...")
                    print("Command:", " ".join(command))
                    subprocess.call(command)

            print("> Done!")

        else:
            print("X Argument --resource-hacker must be provided")


def _getResourceHackerCommand(executablePath, iconPath):
    # type: (_Path, _Path) -> list[str]

    resourceHackerPath = _Path(args.get("--resource-hacker"))
    useWine = platform.system() != "Windows"

    if resourceHackerPath.exists():
        resourceHackerPath = resourceHackerPath.resolve()

        command = ['wine'] if useWine else []
        command += [quote(resourceHackerPath.as_posix())]
        command += ['-open', quote(executablePath.as_posix())]
        command += ['-save', quote(executablePath.as_posix())]
        command += ['-action', 'addoverwrite', '-res', quote(iconPath.as_posix())]
        command += ['-mask', 'ICONGROUP,APPICON,']

        return command

    return []


def quote(value, placeholder='?'):
    # type: (str, str) -> str
    return value.replace(placeholder, data["Quote"])


try:
    main()
except Exception as e:
    print(e)
