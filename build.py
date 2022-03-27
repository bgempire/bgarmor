import sys
import os
import subprocess
import shutil
from pathlib import Path


curDir = Path(__file__).parent.absolute()
pythonExecutable = Path(sys.executable).absolute()


def main():
    # type: () -> None
    
    os.chdir(curDir.as_posix())
    
    if sys.argv[-1] in operators.keys():
        operators[sys.argv[-1]]()
    
    else:
        print("X Invalid command:", sys.argv[-1])
        print("Available commands:", ", ".join([i for i in operators.keys()]))


def build(target):
    # type: (str) -> None
    
    toolchain = "i686-pc-windows-gnu" if target == "windows" else "i686-unknown-linux-gnu"
    ext = ".exe" if target == "windows" else ""
    launcherSourcePath = (curDir / "source/launcher").absolute()
    sourceExe = (curDir / "source/launcher/target/{toolchain}/release/bgarmor{ext}".format(toolchain=toolchain, ext=ext)).absolute()
    targetExe = (curDir / ("release/launcher/Launcher" + ext)).absolute()
    
    print("> Started build for target:", toolchain)
    
    if targetExe.exists():
        print("> Deleted existing executable:", targetExe.as_posix())
        targetExe.unlink()
        
    os.chdir(launcherSourcePath.as_posix())
    args = ["cargo", "build", "--target=" + toolchain, "--release"]
    print("> Running cargo build:", " ".join(args))
    subprocess.call(args)
    os.chdir(curDir.as_posix())
    
    print("> Copying executable to:", targetExe.as_posix())
    shutil.copy2(sourceExe.as_posix(), targetExe.as_posix())
    
    if target != "windows":
        args = ["upx", "-5", targetExe.as_posix()]
        print("> Running upx on executable:", " ".join(args))
        subprocess.call(args)
        
    print("> Done!")


def minify():
    # type: () -> None
    
    script = curDir / "source/scripts/minify_launcher.py"
    subprocess.call([pythonExecutable.as_posix(), script.as_posix()])


def clean():
    # type: () -> None
    
    directory = curDir / "source/launcher/target"
    
    if directory.exists():
        print("> Deleting directory:", directory.as_posix())
        shutil.rmtree(directory.as_posix())


def export():
    # type: () -> None
    
    projectFile = (curDir / "project.godot").absolute()
    exportPath = (curDir / "bin").absolute()
    
    if not exportPath.exists():
        exportPath.mkdir()
        
    targets = {
        "Windows": "Windows Desktop",
        "Linux": "Linux/X11",
    }
    
    for target in targets.keys():
        name = targets[target]
        targetPath = (exportPath / target).absolute()
        
        if targetPath.exists():
            shutil.rmtree(targetPath.as_posix())
        
        targetPath.mkdir()
        
        print("> Exporting for target:", name)
        args = ["godot", "--export", name, "--no-window", projectFile.as_posix()]
        print("> Running Godot export:", " ".join(args))
        subprocess.call(args)
        
        print("> Copying release files to:", targetPath.as_posix())
        shutil.copytree((curDir / "release").as_posix(), (targetPath / "release").as_posix())
    
    print("> Done!")


operators = {
    "windows": lambda: build("windows"),
    "linux": lambda: build("linux"),
    "minify": lambda: minify(),
    "clean": lambda: clean(),
    "export": lambda: export(),
}  # type: dict[str, object]


main()
