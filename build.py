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


operators = {
    "windows": lambda: build("windows"),
    "linux": lambda: build("linux"),
    "minify": lambda: minify(),
    "clean": lambda: clean(),
}  # type: dict[str, object]


main()
