from pathlib import Path as _Path
import common as _common


args = _common.getArgs()
data = _common.getProjectData()


def main():
    # type: () -> None

    import subprocess
    
    print("Run launcher")

    if data:

        if args.get("--engine"):
            ext = ".exe" if args.get("--engine").lower().startswith("windows") else ""
            currentLauncher = data["CurPath"] / ("launcher/Launcher" + ext)  # type: _Path

            if currentLauncher.exists():
                _args = [
                    currentLauncher.as_posix(),
                    "--engine", args.get("--engine"),
                    "--file", args.get("--project"),
                ]
                subprocess.call(_args)

            else:
                print("X Could not find launcher at", currentLauncher.as_posix())

        else:
            print("X Argument --engine must be provided")

try:
    main()

except Exception as e:
    print(e)
