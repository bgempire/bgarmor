import os
import platform
import subprocess
import shutil
from pathlib import Path
from ast import literal_eval
from pprint import pprint
import common

data = common.getData()

print("---------------------------------")
print("BGArmor Release Builder - " + platform.system())
print("---------------------------------")
print("\nThis script will generate builds for the selected available\nplatforms. These releases can be compressed as well.")

def getAvailableTargets(path):
    availableTargets = {"All" : None}
    for _dir in path.iterdir():
        if _dir.is_dir():
            for _file in _dir.iterdir():
                if _file.name == "engine_executable.txt":
                    engineExecutablePath = None
                    try:
                        with open(_file.as_posix(), "r") as sourceFile:
                            engineExecutablePath = literal_eval(sourceFile.read().split("=")[1])
                    except:
                        pass
                    if engineExecutablePath is not None:
                        targetPath = Path(engineExecutablePath)
                        if targetPath.exists():
                            availableTargets[targetPath.parent.name] = targetPath.parent.resolve()
                            
    return availableTargets

if data is not None:
    availableTargets = getAvailableTargets(data["CurPath"] / "launcher")
    targets = None
    compress = False
    
    while True:
        validTargets = True
        availableTargetsList = list(availableTargets.keys())
        availableTargetsList.sort()
        print("\n> Available release targets:", ", ".join(availableTargetsList))
        targets = input("> Input the release targets (separated by space): ").split(" ")
        targets = [i.capitalize() for i in targets]
        
        for target in targets:
            if target != "All" and not target in availableTargets.keys():
                print("X Target not available:", target)
                validTargets = False
                
        if validTargets:
            break
            
    if "All" in targets:
        targets = list(availableTargets.keys())
        targets.remove("All")
        
    while True:
        answer = input("> Compress the selected targets? (Y/N): ").upper()
        if answer in ("Y", "N"):
            compress = True if answer == "Y" else False
            break
        else:
            print("X Invalid answer! Must be Y or N")
    
    releaseDir = data["CurPath"] / "release"
    
    if not releaseDir.exists():
        releaseDir.mkdir()
        print("> Directory of release created:", releaseDir.as_posix())
        
    archiveExt = "zip"
    launcherDir = Path(data["CurPath"]) / "launcher"
    engineDir = Path(data["CurPath"]) / "engine"
    dataFile = Path(data["DataFile"]).resolve()
    
    if releaseDir.exists() and dataFile.exists() and launcherDir.exists():
        
        for target in targets:
            print("")
            hasErrors = False
            
            print("> Building target:", target)
            launcherExt = ".exe" if "Windows" in target else ""
            releaseTargetPath = releaseDir / ("-".join([common.formatFileName(data["GameName"], spaces=False), data["Version"], target]))
            releaseTargetLauncherPath = releaseTargetPath / "launcher"
            releaseTargetEnginePath = releaseTargetPath / "engine"
            
            shutil.rmtree(releaseTargetPath.as_posix(), True)
            
            if not releaseTargetPath.exists():
                print("    > Creating directory:", releaseTargetPath.as_posix())
                releaseTargetPath.mkdir()
                releaseTargetLauncherPath.mkdir()
                releaseTargetEnginePath.mkdir()
                
            print("    > Copying data file to:", (releaseTargetPath / dataFile.name).as_posix())
            shutil.copy(dataFile.as_posix(), (releaseTargetPath / dataFile.name).as_posix())
            
            print("    > Copying launcher files to:", (releaseTargetLauncherPath / target).as_posix())
            shutil.copytree((launcherDir / target).as_posix(), (releaseTargetLauncherPath / target).as_posix())
            for _file in launcherDir.iterdir():
                if not _file.is_dir():
                    shutil.copy(_file.as_posix(), releaseTargetLauncherPath.as_posix())
                    
            print("    > Copying engine files to:", (releaseTargetEnginePath / target).as_posix())
            shutil.copytree((engineDir / target).as_posix(), (releaseTargetEnginePath / target).as_posix())
            
            launcherExecutable = None
            for _file in data["CurPath"].iterdir():
                if not _file.is_dir():
                    if _file.name in ("BGArmor" + launcherExt, data["GameName"] + launcherExt):
                        launcherExecutable = _file
                        break
                        
            if launcherExecutable is not None:
                launcherExecutableTarget = releaseTargetPath / (common.formatFileName(data["GameName"]) + launcherExt)
                print("    > Copying launcher executable to:", launcherExecutableTarget.as_posix())
                shutil.copy(
                    launcherExecutable.as_posix(), 
                    launcherExecutableTarget.as_posix()
                )
                
            elif launcherExecutable is None:
                hasErrors = True
                print("    X Could not find launcher executable for " + target + " on:", data["CurPath"])
                
            if compress:
                if not hasErrors:
                    print("    > Compressing target release to:", releaseTargetPath.as_posix() + "." + archiveExt)
                    os.chdir(releaseTargetPath.parent.as_posix())
                    shutil.make_archive(
                        releaseTargetPath.name, 
                        archiveExt, 
                        releaseTargetPath.parent.as_posix(), 
                        releaseTargetPath.name
                    )
                    os.chdir(data["CurPath"].as_posix())
                else:
                    print("    > Errors happened, will not compress this release")
            
            print("    > Build successful:", target)
