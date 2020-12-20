import bge
from bge.logic import globalDict
from bge.render import getWindowWidth, getWindowHeight

def setViewport(cont):
	''' On Map scene start, enables viewport and sets the viewport 
	coordinates to top right.
	
	Blend: Main.blend / Scene: Minimap / Object: PlayerArrow '''
	
	# Objects
	own = cont.owner
	camera = own.scene.active_camera
	
	# Sensors
	sensor = cont.sensors[0]
	
	sceneNames = [scn.name for scn in bge.logic.getSceneList()]
	
	### PROCESS ###
	if sensor.positive and "Game" in sceneNames:
		
		# Enable viewport use on map camera
		camera.useViewport = True
		
		# Pre process the viewport pixel coordinates
		left = getWindowWidth() // 2
		bottom = getWindowHeight() // 2
		right = getWindowWidth()
		top = getWindowHeight()
		
		# Set viewport coordinates
		camera.setViewport(left, bottom, right, top)
		
		print('Viewport set: \nleft =', left, '| right =', right, '| top =', top, '| bottom =', bottom)
		
def updateArrow(cont):
	''' Constantly updates the map arrow's position and rotation 
	from values previously stored on globalDict.
	
	Blend: Main.blend / Scene: Minimap / Object: PlayerArrow '''
	
	# Objects
	own = cont.owner
	
	# Sensors
	sensor = cont.sensors[0]
	
	### PROCESS ###
	if sensor.positive:
		
		# Check if values are present in globalDict
		if 'Position' in globalDict.keys() and 'Rotation' in globalDict.keys():
			
			# Update arrow's position and rotation
			own.worldPosition = globalDict['Position']
			own.localOrientation = globalDict['Rotation']