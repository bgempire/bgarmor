import zipfile
import zlib
import os
import sys
import string
import shutil
import glob
import ctypes
import subprocess
import platform

from pathlib import Path
from ast import literal_eval
from pprint import pprint

_DEBUG = 0
curPath = Path(__file__).resolve().parent
curPlatform = platform.system()
PLAT_QUOTE = '"' if platform.system() == "Windows" else "'"

def processMetadata(path):
	metadata = None
	metaSourcePath = path / "metadata.txt"
	metaPath = path / "metadata.dat"
	
	if metaSourcePath.exists():
		with open(metaSourcePath.as_posix(), "r") as sourceFile:
			metadata = sourceFile.read()
			with open(metaPath.as_posix(), "wb") as targetFile:
				targetFile.write(zlib.compress(metadata.encode(), zlib.Z_BEST_COMPRESSION))
				print("> Written metadata to", metaPath.as_posix())
	
	elif metaPath.exists():
		with open(metaPath.as_posix(), "rb") as sourceFile:
			metadata = zlib.decompress(sourceFile.read()).decode()
			print("> Read metadata from", metaPath.as_posix())
	else:
		print("X Metadata not found, will continue without it")
		
	return metadata
	
def loadConfig(path):
	config = None
	configPath = path / (curPlatform + "/config.json")
	
	if configPath.exists():
		with open(configPath.as_posix(), "r") as sourceFile:
			config = literal_eval(sourceFile.read())
			print("> Read config from", configPath.as_posix())
	
	return config

def getGameDir(config):
	
	def getGameDirName(name):
		result = ""
		name = name.lower()
		allowedChars = string.ascii_lowercase + " "
		for c in name:
			if c in allowedChars:
				result += c
		return "." + result.replace(" ", "-")
		
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

metadata = processMetadata(curPath)
config = loadConfig(curPath)

if metadata is not None and config is not None:
	gameDir = getGameDir(config)
	dataPath = curPath.parent / config["DataFile"]
	
	if dataPath.exists():
		dataPath = dataPath.resolve()
		tempPath = gameDir / ".temp"
		
		# Create temporary directory to extract game data
		tempPath.mkdir(parents=True, exist_ok=True)
		
		# Extract game data into temp directory
		gameData = zipfile.ZipFile(dataPath.as_posix(), mode='r')
		gameData.extractall(path=tempPath.as_posix(), pwd=metadata.encode())
		
		filesLists = getFilesLists(tempPath)
		persistentFiles = filesLists[0]
		generalFiles = filesLists[1]
		
		persistentFilesTarget = []
		generalFilesTarget = []
		
		if _DEBUG:
			print("> Move files from temp directory to game directory...")
			os.system("PAUSE")
		
		# Move files from temp directory to game directory
		moveFilesToMain()
		
		if _DEBUG:
			print("> Remove temp directory after moving files...")
			os.system("PAUSE")
		
		# Remove temp directory after moving files
		shutil.rmtree(tempPath.as_posix(), ignore_errors=True)
		
		filesLists = getFilesLists(gameDir)
		persistentFiles = filesLists[0]
		generalFiles = filesLists[1]
		
		enginePath = curPath.parent / config["EnginePath"]
		command = PLAT_QUOTE + enginePath.as_posix() + PLAT_QUOTE + " " + PLAT_QUOTE + config["MainFile"] + PLAT_QUOTE
		os.chdir(gameDir.as_posix())
		subprocess.call(command, shell=True)
		
		if _DEBUG:
			print("> Remove all files before finish...")
			os.system("PAUSE")
		
		# Remove all files before finish
		for _file in generalFiles:
			_file.unlink()
			
		# Remove all empty directories before finish
		removeEmptyDirs(gameDir)
