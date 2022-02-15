extends Control


onready var globals = $"/root/Globals"


func _ready() -> void:
	var app_name = ProjectSettings.get_setting("application/config/name")
	var game_name = globals.current_project_data.get("GameName", "")
	
	if game_name:
		OS.set_window_title(app_name + " - " + game_name)
		
	else:
		OS.set_window_title(app_name)


func _on_ButtonCloseProject_pressed() -> void:
	globals.current_project_data.clear()
	globals.current_project_path = ""
	get_tree().change_scene("res://scenes/welcome.tscn")
