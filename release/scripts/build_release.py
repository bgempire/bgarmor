import common as _common
from pathlib import Path


ARCHIVE_EXT = "zip"

args = _common.getArgs()
data = _common.getProjectData()


def main():
    # type: () -> None

    print("Started game release build")

    if data:
        _performRelease()


def _performRelease():
    # type: () -> None

    import os
    import shutil

    curPath = data["CurPath"]  # type: Path
    targets = [args.get("--target")] if args.get("--target") else []  # type: list[str]
    compress = args.get("--compress", False)

    if "All" in targets:
        targets = [i for i in data["EngineExecutables"].keys()]

    releaseDir = curPath / "release"  # type: Path

    if not releaseDir.exists():
        releaseDir.mkdir()
        print("> Directory of release created:", releaseDir.as_posix())

    launcherDir = curPath / "launcher"
    engineDir = curPath / "engine"
    dataFile = curPath / data["DataFile"]  # type: Path

    if not releaseDir.exists():
        print("X Release directory do not exist:", releaseDir)
        return

    elif not dataFile.exists():
        print("X Data file do not exist:", dataFile)
        return

    elif not launcherDir.exists():
        print("X Launcher directory do not exist:", launcherDir)
        return

    elif not targets:
        print("X At least one target must be specified")
        return

    else:

        for target in targets:
            hasErrors = False

            print("\n> Building target:", target)
            launcherExt = ".exe" if "Windows" in target else ""
            releaseTargetPath = releaseDir / ("-".join([_common.formatFileName(data["GameName"], spaces=False), data["Version"], target]))
            releaseTargetLauncherPath = releaseTargetPath / "launcher"
            releaseTargetEnginePath = releaseTargetPath / "engine"

            if releaseTargetPath.exists():
                print("    > Removing existing directory:", releaseTargetPath)
                shutil.rmtree(releaseTargetPath.as_posix(), True)

            if not releaseTargetPath.exists():
                print("    > Creating directory:", releaseTargetPath)
                releaseTargetPath.mkdir()
                releaseTargetLauncherPath.mkdir()
                releaseTargetEnginePath.mkdir()

            print("    > Copying data file to:", releaseTargetPath / dataFile.name)
            shutil.copy2(dataFile.as_posix(), (releaseTargetPath / dataFile.name).as_posix())

            print("    > Copying launcher files from:", launcherDir)
            print("        > Copying launcher script to:", releaseTargetLauncherPath / "launcher.py")
            shutil.copy2((launcherDir / "launcher.py").as_posix(), (releaseTargetLauncherPath / "launcher.py").as_posix())
            print("        > Copying launcher config:", releaseTargetLauncherPath / "config.json")
            shutil.copy2(Path(data["ProjectFile"]).as_posix(), (releaseTargetLauncherPath / "config.json").as_posix())

            launcherExecutable = None  # type: Path

            for _file in launcherDir.iterdir():
                if not _file.is_dir() and _file.suffix == launcherExt:
                    launcherExecutable = _file
                    break

            if launcherExecutable:
                launcherExecutableTarget = releaseTargetPath / (_common.formatFileName(data["GameName"]) + launcherExt)
                print("        > Copying launcher executable to:", launcherExecutableTarget)
                shutil.copy2(launcherExecutable.as_posix(), launcherExecutableTarget.as_posix())

            else:
                hasErrors = True
                print("        X Could not find launcher executable for " + target + " on:", launcherDir)

            print("    > Copying engine files to:", releaseTargetEnginePath / target)
            shutil.copytree((engineDir / target).as_posix(), (releaseTargetEnginePath / target).as_posix())

            if compress:
                if not hasErrors:
                    print("    > Compressing target release to:", releaseTargetPath.as_posix() + "." + ARCHIVE_EXT)
                    os.chdir(releaseTargetPath.parent.as_posix())
                    shutil.make_archive(releaseTargetPath.name, ARCHIVE_EXT, releaseTargetPath.parent.as_posix(), releaseTargetPath.name)
                    os.chdir(curPath.as_posix())
                else:
                    print("    > Errors happened, will not compress this release")

            print("    > Build successful:", target)


try:
    main()
except Exception as e:
    print(e)
