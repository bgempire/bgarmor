import zlib
import bge
from bge.logic import globalDict
from pathlib import Path
from ast import literal_eval

SAVE_INTERVAL = 10.0 # Seconds

def saveGame(cont):
	""" Saves the game at a fixed period of time.
	
	Blend: LibPlayer.blend / Scene: _LibScenery / Object: PlayerCollision """
	
	# Objects
	own = cont.owner
	
	# Sensors
	sensor = cont.sensors[0]
	
	### PROCESS ###
	if sensor.positive and not own.scene.name.startswith("_Lib"):
		
		sensor.skippedTicks = int(SAVE_INTERVAL * 60)
		
		# Properties
		saveFile = Path(bge.logic.expandPath("//save.sav"))
		saveData = {
			"Position" : list(own.worldPosition),
			"Rotation" : list(own.worldOrientation.to_euler())
		}
		
		# Load game at start if save file exists
		if sensor.status == 1 and saveFile.exists():
			try:
				with open(saveFile.as_posix(), "rb") as openedFile:
					saveData = zlib.decompress(openedFile.read())
					saveData = literal_eval(saveData.decode())
					
				own.worldPosition = saveData["Position"]
				own.worldOrientation = saveData["Rotation"]
				own.sendMessage("Notification", "AutoLoaded")
				print("> Player loaded at position: {pos}, rotation: {rot}".format(
					pos=saveData["Position"], rot=saveData["Rotation"]))
			except:
				print("X Could read file from: ", saveFile.as_posix())
		else:
			try:
				with open(saveFile.as_posix(), "wb") as openedFile:
					openedFile.write(zlib.compress(str(saveData).encode()))
					print("> Player saved at position: {pos}, rotation: {rot}".format(
						pos=saveData["Position"], rot=saveData["Rotation"]))
					own.sendMessage("Notification", "AutoSaved")
			except:
				print("X Could not save file to: ", saveFile.as_posix())

def setProps(cont):
	""" Get player position and rotation and store on globalDict.
	
	Blend: LibPlayer.blend / Scene: _LibScenery / Object: PlayerCollision """
	
	# Objects
	own = cont.owner
	
	# Sensors
	sensor = cont.sensors[0]
	
	### PROCESS ###
	if sensor.positive:
		
		# Add minimap scene at start
		if sensor.status == 1:
			bge.logic.addScene("Hud", 1)
			bge.logic.addScene("Minimap", 1)
		
		# Store player position and rotation on globalDict
		globalDict["Position"] = list(own.worldPosition)
		globalDict["Rotation"] = list(own.localOrientation.to_euler())

