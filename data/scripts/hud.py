import bge
from bge.logic import globalDict

NOTIFICATION_TEXTS = {
	"AutoLoaded" : "The game was auto loaded.",
	"AutoSaved" : "The game was auto saved."
}

def notificationText(cont):
	''' Shows a message on HUD in each notification received through messages.
	
	Blend: Main.blend / Scene: Hud / Object: NotificationText '''
	
	# Objects
	own = cont.owner
	
	# Sensors
	sensor = cont.sensors[0]
	
	### PROCESS ###
	if sensor.positive:
		for body in sensor.bodies:
			if body in NOTIFICATION_TEXTS.keys():
				own.text = NOTIFICATION_TEXTS[body]
			else:
				own.text = body
			own.playAction("ObjColorFade", 0, 60)