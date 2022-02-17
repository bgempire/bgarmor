extends Control

const NODE_FIELD_RELATIONS = [
	{
		"node": "LineEditGameName",
		"field": "GameName",
		"property": "text",
	},
	{
		"node": "LineEditVersion",
		"field": "Version",
		"property": "text",
	},
	{
		"node": "ButtonMainFile",
		"field": "MainFile",
		"property": "text",
	},
	{
		"node": "ButtonDataFile",
		"field": "DataFile",
		"property": "text",
	},
	{
		"node": "ButtonDataSource",
		"field": "DataSource",
		"property": "text",
	},
	{
		"node": "SpinBoxDataChunkSize",
		"field": "DataChunkSize",
		"property": "value",
	},
	{
		"node": "ButtonEngineWindows32",
		"field": "EngineWindows32",
		"property": "text",
	},
	{
		"node": "ButtonEngineWindows64",
		"field": "EngineWindows64",
		"property": "text",
	},
	{
		"node": "ButtonEngineLinux32",
		"field": "EngineLinux32",
		"property": "text",
	},
	{
		"node": "ButtonEngineLinux64",
		"field": "EngineLinux64",
		"property": "text",
	},
	{
		"node": "ButtonPythonWindows32",
		"field": "PythonWindows32",
		"property": "text",
	},
	{
		"node": "ButtonPythonWindows64",
		"field": "PythonWindows64",
		"property": "text",
	},
	{
		"node": "ButtonPythonLinux32",
		"field": "PythonLinux32",
		"property": "text",
	},
	{
		"node": "ButtonPythonLinux64",
		"field": "PythonLinux64",
		"property": "text",
	},
	{
		"node": "ItemListPersistent",
		"field": "Persistent",
		"is_item_list": true,
	},
	{
		"node": "ItemListIgnore",
		"field": "Ignore",
		"is_item_list": true,
	},
]

onready var globals = $"/root/Globals"


func _ready() -> void:
	var app_name = ProjectSettings.get_setting("application/config/name")
	var game_name = globals.current_project_data.get("GameName", "")
	
	if game_name:
		OS.set_window_title(app_name + " - " + game_name)
		
	else:
		OS.set_window_title(app_name)
		
	_update_fields()


func _on_ButtonCloseProject_pressed() -> void:
	globals.current_project_data.clear()
	globals.current_project_path = ""
	get_tree().change_scene("res://scenes/welcome.tscn")


func _update_fields():
	var cur_project = globals.current_project_data
	var default = globals.DEFAULT_FIELDS
	
	for field in NODE_FIELD_RELATIONS:
		var cur_node = $".".find_node(field["node"])
		
		if cur_node:
			
			if field.get("is_item_list"):
				var item_list: ItemList = cur_node
				
				for item in cur_project.get(field["field"], default[field["field"]]):
					item_list.add_item(item)
				
			else:
				var control: Control = cur_node
				
				control.set(
					field["property"], 
					cur_project.get(field["field"], default[field["field"]])
				)
		else:
			print("Could not find node: " + field["node"])

