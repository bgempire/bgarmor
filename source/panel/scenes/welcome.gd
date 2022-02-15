extends Control

onready var globals = $"/root/Globals"


func _ready() -> void:
	OS.set_window_title(ProjectSettings.get_setting("application/config/name"))
	var home_dir = OS.get_environment('HOME')
	$FileDialogNew.current_dir = home_dir
	$FileDialogOpen.current_dir = home_dir


func _on_ButtonNew_pressed() -> void:
	$FileDialogNew.popup()


func _on_ButtonOpen_pressed() -> void:
	$FileDialogOpen.popup()


func _on_ButtonDocs_pressed() -> void:
	OS.shell_open("https://bgempire.github.io/bgarmor/")


func _on_ButtonSource_pressed() -> void:
	OS.shell_open("https://github.com/bgempire/bgarmor")


func _on_FileDialogOpen_file_selected(path: String) -> void:
	var file = File.new()
	file.open(path, File.READ)
	var file_data = JSON.parse(globals.get_json_no_comments(file.get_as_text()))
	file.close()
	
	if file_data.error == OK:
		file_data = file_data.result
		
		if validate_data(file_data):
			globals.current_project_path = path
			globals.current_project_data = file_data
			get_tree().change_scene("res://scenes/editor.tscn")
			
		else:
			$AcceptDialog.dialog_text = "Invalid project file data:\n" + path
			$AcceptDialog.popup_centered()
		
	else:
		$AcceptDialog.dialog_text = "Could not read file:\n" + path
		$AcceptDialog.popup_centered()


func validate_data(data: Dictionary) -> bool:
	
	# Validate fields on loaded data
	for key in data.keys():
		if not key in globals.DEFAULT_FIELDS.keys():
			return false
	
	# Add non existent fields to loaded data
	for key in globals.DEFAULT_FIELDS.keys():
		if not key in data.keys():
			data[key] = globals.DEFAULT_FIELDS[key]
	
	return true
