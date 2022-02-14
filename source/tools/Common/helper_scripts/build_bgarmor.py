import os
import platform
import subprocess
import shutil
import glob
from pathlib import Path
from ast import literal_eval
from pprint import pprint

import common

data = common.getData()

if data is not None:
    compress = False
    releaseFilesList = data["CurPath"] / "source/release_files.py"
    targetPath = (data["CurPath"] / "release") / common.formatFileName(
        "bgarmor-v" + data["Version"] + " Win Linux",
        spaces=False,
        lowercase=True
    )
    if targetPath.exists():
        shutil.rmtree(targetPath.as_posix(), ignore_errors=True)
        print("> Existing folder deleted:", targetPath.as_posix())
        
    if not targetPath.exists():
        targetPath.mkdir(parents=True)
        print("> Folder created at:", targetPath.as_posix())
    
    if releaseFilesList.exists():
        with open(releaseFilesList.as_posix(), "r") as sourceFile:
            releaseFilesList = literal_eval(sourceFile.read())
            print("> Read release files list from:", sourceFile.name)
            
        print("\n> Creating new files and folders:")
        for _path in releaseFilesList["Create"]:
            elementType = "folder" if _path.endswith("/") else "file"
            path = targetPath / _path
            if elementType == "folder" and not path.exists():
                path.mkdir(parents=True)
            else:
                path.touch()
            print("    > Created", elementType, "at:", path.as_posix())
            
        print("\n> Copying existing files and folders:")
        for _path in releaseFilesList["Copy"]:
            elementType = "folder" if _path.endswith("/") else "file"
            path = targetPath / _path
            sourcePath = data["CurPath"] / _path
            
            if not sourcePath.exists():
                print("    X Could not find", elementType + ":", sourcePath.as_posix())
                continue
                
            if elementType == "folder" and not path.exists():
                shutil.copytree(sourcePath.as_posix(), path.as_posix())
            else:
                shutil.copy2(sourcePath.as_posix(), path.as_posix())
                
            print("    > Copied", elementType, "to:", path.as_posix())
        
        print("\n> Removing unnecessary files and folders:")
        for pattern in releaseFilesList["Delete"]:
            for _path in glob.glob(targetPath.as_posix() + "/**/" + pattern, recursive=True):
                _path = Path(_path)
                if _path.is_dir():
                    shutil.rmtree(_path.as_posix(), ignore_errors=True)
                else:
                    _path.unlink()
                print("    > Removed:", _path)
    
