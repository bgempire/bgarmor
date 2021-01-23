import zlib
import os
import sys
import string
import shutil
import glob
import base64
import subprocess
import platform

from pathlib import Path
from ast import literal_eval
from time import time

_DEBUG = False
PLAT_QUOTE = '"' if platform.system() == "Windows" else "'"

curPath = Path(__file__).resolve().parent
curPlatform = platform.system()

if curPath.name == "source":
    curPath = curPath.parent / "launcher"
    os.chdir(curPath.as_posix())
    
def loadConfig(path):
    config = None
    configPath = path / "config.json"
    engineCandidates = [curPlatform, curPlatform + "32", curPlatform + "64"]
    enginePath = None
    
    for _path in engineCandidates:
        _path = path / (_path + "/engine_executable.txt")
        if _path.exists():
            enginePath = _path.resolve()
            break
    
    if configPath.exists() and enginePath is not None:
        with open(configPath.as_posix(), "r") as sourceFile:
            config = literal_eval(sourceFile.read())
            print("> Read config from", configPath.as_posix())
            
        if enginePath.exists():
            with open(enginePath.as_posix(), "r") as sourceFile:
                enginePathRead = eval(sourceFile.read().split('=')[-1])
                
                if enginePathRead:
                    config["EnginePath"] = enginePathRead
                    print("> Read engine path from", enginePath.as_posix())
            
            return config

def getGameDir(config):
    
    def getGameDirName(name):
        result = ""
        allowedChars = string.ascii_lowercase + string.ascii_uppercase + " -"
        for c in name:
            if c in allowedChars:
                result += c
        return "." + result
        
    gameDir = Path.home()
    gameName = getGameDirName(config["GameName"])
    
    # Get game directory in a cross platform way
    if sys.platform == "win32":
        gameDir = gameDir / ("AppData/Roaming/" + gameName)
    elif sys.platform == "linux":
        gameDir = gameDir / (".local/share/" + gameName)
    elif sys.platform == "darwin":
        gameDir = gameDir / ("Library/Application Support/" + gameName)
        
    # Create game directory
    gameDir.mkdir(parents=True, exist_ok=True)
    
    # Hide game directory on Windows
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.kernel32.SetFileAttributesW(gameDir.as_posix(), 2)
        
    return gameDir
    
def getFilesLists(path):
        persistentFiles = []
        generalFiles = []
        
        # Populate persistent files list
        for pattern in config["Persistent"]:
            persistentFiles += [Path(p).resolve() for p in glob.glob(
                path.as_posix() + "/**/" + pattern, recursive=True)]
        
        # Populate general files list
        generalFiles += [Path(p).resolve() for p in glob.glob(
                path.as_posix() + "/**/*", recursive=True)
                if Path(p).is_file()]
        
        # Remove persistent files from general files list
        for pers in persistentFiles:
            for gen in generalFiles:
                if pers.samefile(gen):
                    generalFiles.remove(gen)
                    
        return [persistentFiles, generalFiles]

def ensurePath(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

def decompressDataFile(dataFile, targetPath):
    startTime = time()
    
    if targetPath.exists():
        shutil.rmtree(targetPath.as_posix())
        
    if not targetPath.exists():
        targetPath.mkdir()
    
    if dataFile.exists():
        curLineType = "Path"
        filePath = None
        print("\n> Decompressing data file from", dataFile.as_posix())
        
        for line in open(dataFile.as_posix(), "rb"):
            if curLineType == "Path":
                filePath = (targetPath / base64.b64decode(line).decode())
                curLineType = "Data"
            else:
                if not filePath.parent.exists():
                    try:
                        os.makedirs(filePath.parent.as_posix())
                    except:
                        pass
                with open(filePath.as_posix(), "wb") as targetFileObj:
                    targetFileObj.write(zlib.decompress(base64.b64decode(line)))
                    
                curLineType = "Path"
                
    print("> Done! Time taken:", round(time() - startTime, 3), "seconds\n")

def moveFilesToMain():
    # Move general files to game directory if not already exists
    for _file in generalFiles:
        _fileTarget = Path(_file.as_posix().replace(".temp/", ""))
        if not _fileTarget.exists():
            _file.rename(ensurePath(_fileTarget))
            generalFilesTarget.append(_fileTarget.resolve())
    
    # Move persistent files to game directory if not already exists
    for _file in persistentFiles:
        _fileTarget = Path(_file.as_posix().replace(".temp/", ""))
        if not _fileTarget.exists():
            _file.rename(ensurePath(_fileTarget))
            persistentFilesTarget.append(_fileTarget.resolve())

def removeEmptyDirs(path):
    for root, dirs, files in os.walk(path.as_posix(), topdown=False):
        root = Path(root).resolve()
        for _dir in dirs:
            _dir = root / _dir
            try:
                _dir.rmdir()
            except:
                pass

config = loadConfig(curPath)

if config is not None:
    gameDir = getGameDir(config)
    dataPath = curPath.parent / config["DataFile"]
    
    if dataPath.exists():
        dataPath = dataPath.resolve()
        tempPath = gameDir / ".temp"
        
        if _DEBUG:
            print("> Extract game data into temp directory...")
            input("Press any key to continue...")
        
        # Extract game data into temp directory
        decompressDataFile(dataPath, tempPath)
        
        filesLists = getFilesLists(tempPath)
        persistentFiles = filesLists[0]
        generalFiles = filesLists[1]
        
        persistentFilesTarget = []
        generalFilesTarget = []
        
        if _DEBUG:
            print("> Move files from temp directory to game directory...")
            input("Press any key to continue...")
        
        # Move files from temp directory to game directory
        moveFilesToMain()
        
        if _DEBUG:
            print("> Remove temp directory after moving files...")
            input("Press any key to continue...")
        
        # Remove temp directory after moving files
        shutil.rmtree(tempPath.as_posix(), ignore_errors=True)
        
        filesLists = getFilesLists(gameDir)
        persistentFiles = filesLists[0]
        generalFiles = filesLists[1]
        enginePath = curPath.parent / config["EnginePath"]
        
        if platform.system() != "Windows":
            os.system("chmod +x " + PLAT_QUOTE + enginePath.as_posix() + PLAT_QUOTE)
            
        extraArgs = " " + " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
        command = PLAT_QUOTE + enginePath.as_posix() + PLAT_QUOTE + extraArgs + " " + PLAT_QUOTE + config["MainFile"] + PLAT_QUOTE
        os.chdir(gameDir.as_posix())
        subprocess.call(command, shell=True)
        
        if _DEBUG:
            print("> Remove all files before finish...")
            input("Press any key to continue...")
        
        # Remove all files before finish
        for _file in generalFiles:
            _file.unlink()
            
        # Remove all empty directories before finish
        removeEmptyDirs(gameDir)
        
    else:
        print("X Could not find game data at", dataPath.as_posix())
