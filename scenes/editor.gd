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
		"node": "LineEditMainFile",
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

var BUTTON_FILE_DIALOG_RELATIONS = [
	{
		"node": "ButtonDataFile",
		"field": "DataFile",
		"filters": PoolStringArray(["*.dat ; Data File"]),
		"mode": FileDialog.MODE_SAVE_FILE,
		"title": "Select the game package data file"
	},
	{
		"node": "ButtonDataSource",
		"field": "DataSource",
		"filters": PoolStringArray(["*.* ; Data Source"]),
		"mode": FileDialog.MODE_OPEN_DIR,
		"title": "Select the game source data directory"
	},
	{
		"node": "ButtonEngineWindows32",
		"field": "EngineWindows32",
		"filters": PoolStringArray(["*.exe ; Executable"]),
		"mode": FileDialog.MODE_OPEN_FILE,
		"title": "Select the engine executable"
	},
	{
		"node": "ButtonEngineWindows64",
		"field": "EngineWindows64",
		"filters": PoolStringArray(["*.exe ; Executable"]),
		"mode": FileDialog.MODE_OPEN_FILE,
		"title": "Select the engine executable"
	},
	{
		"node": "ButtonEngineLinux32",
		"field": "EngineLinux32",
		"filters": PoolStringArray(["* ; Executable"]),
		"mode": FileDialog.MODE_OPEN_FILE,
		"title": "Select the engine executable"
	},
	{
		"node": "ButtonEngineLinux64",
		"field": "EngineLinux64",
		"filters": PoolStringArray(["* ; Executable"]),
		"mode": FileDialog.MODE_OPEN_FILE,
		"title": "Select the engine executable"
	},
	{
		"node": "ButtonPythonWindows32",
		"field": "PythonWindows32",
		"filters": PoolStringArray(["*.exe ; Executable"]),
		"mode": FileDialog.MODE_OPEN_FILE,
		"title": "Select the Python executable"
	},
	{
		"node": "ButtonPythonWindows64",
		"field": "PythonWindows64",
		"filters": PoolStringArray(["*.exe ; Executable"]),
		"mode": FileDialog.MODE_OPEN_FILE,
		"title": "Select the Python executable"
	},
	{
		"node": "ButtonPythonLinux32",
		"field": "PythonLinux32",
		"filters": PoolStringArray(["* ; Executable"]),
		"mode": FileDialog.MODE_OPEN_FILE,
		"title": "Select the Python executable"
	},
	{
		"node": "ButtonPythonLinux64",
		"field": "PythonLinux64",
		"filters": PoolStringArray(["* ; Executable"]),
		"mode": FileDialog.MODE_OPEN_FILE,
		"title": "Select the Python executable"
	},
]

onready var globals: BGArmorGlobals = $"/root/Globals"


func _ready() -> void:
	var app_name = ProjectSettings.get_setting("application/config/name")
	var game_name = globals.current_project_data.get("GameName", "")
	
	if game_name:
		OS.set_window_title(app_name + " - " + game_name)
		
	else:
		OS.set_window_title(app_name)
		
	_update_fields()
	_connect_line_edits()
	_connect_file_buttons()
	var _error = $FileDialog.connect("dir_selected", self, "_on_FileDialog_any_selected")
	_error = $FileDialog.connect("file_selected", self, "_on_FileDialog_any_selected")


func _on_ButtonSave_pressed() -> void:
	globals.save_project()


func _on_ButtonCloseProject_pressed() -> void:
	globals.current_project_data.clear()
	globals.current_project_path = ""
	globals.current_project_dir = ""
	var _error = get_tree().change_scene("res://scenes/welcome.tscn")


func _on_ButtonAddPersistent_pressed() -> void:
	var line_edit: LineEdit = find_node("LineEditPersistent")
	var item_list: ItemList = find_node("ItemListPersistent")
	
	if line_edit.text:
		item_list.add_item(line_edit.text)
		globals.current_project_data["Persistent"] = _get_item_list(item_list)
		line_edit.text = ""


func _on_ButtonDelPersistent_pressed() -> void:
	var item_list: ItemList = find_node("ItemListPersistent")
	
	if item_list.get_selected_items():
		item_list.remove_item(item_list.get_selected_items()[0])
		globals.current_project_data["Persistent"] = _get_item_list(item_list)


func _on_ButtonAddIgnore_pressed() -> void:
	var line_edit: LineEdit = find_node("LineEditIgnore")
	var item_list: ItemList = find_node("ItemListIgnore")
	
	if line_edit.text:
		item_list.add_item(line_edit.text)
		globals.current_project_data["Ignore"] = _get_item_list(item_list)
		line_edit.text = ""


func _on_ButtonDelIgnore_pressed() -> void:
	var item_list: ItemList = find_node("ItemListIgnore")
	
	if item_list.get_selected_items():
		item_list.remove_item(item_list.get_selected_items()[0])
		globals.current_project_data["Ignore"] = _get_item_list(item_list)


func _on_LineEdit_text_changed(new_text: String, line_edit: LineEdit, field: String) -> void:
	
	if new_text:
		globals.current_project_data[field] = line_edit.text


func _on_SpinBoxDataChunkSize_value_changed(value: float) -> void:
	globals.current_project_data["DataChunkSize"] = int(value)


func _on_FileButton_pressed(data: Dictionary) -> void:
	var file_dialog = $FileDialog
	file_dialog.mode = data["mode"]
	file_dialog.filters = data["filters"]
	file_dialog.window_title = data["title"]
	file_dialog.current_dir = globals.current_project_dir
	file_dialog.dialog_text = data["node"]
	file_dialog.popup_centered()


func _on_FileDialog_any_selected(path: String) -> void:
	
	if globals.current_project_dir in path:
		var field_name = $FileDialog.dialog_text.replace("Button", "")
		var button: Button = find_node($FileDialog.dialog_text)
		var relative_path = path.replace(globals.current_project_dir, ".")
		globals.current_project_data[field_name] = relative_path
		button.text = relative_path
		
	else:
		$AcceptDialog.dialog_text = "Path must be inside project folder!"
		$AcceptDialog.popup_centered()


func _update_fields() -> void:
	var cur_project = globals.current_project_data
	var default = globals.DEFAULT_FIELDS
	
	for field in NODE_FIELD_RELATIONS:
		var cur_node = find_node(field["node"])
		
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


func _connect_line_edits() -> void:
	var nodes = globals.find_by_class(self, "LineEdit")
	
	for node in nodes:
		var field = node.name.replace("LineEdit", "")
		
		if globals.current_project_data.get(field) is String:
			var line_edit: LineEdit = node
			
			var _error = line_edit.connect("text_changed", self, "_on_LineEdit_text_changed", [line_edit, field])


func _connect_file_buttons() -> void:
	
	for field in BUTTON_FILE_DIALOG_RELATIONS:
		var button: Button = find_node(field["node"])
		var _error = button.connect("pressed", self, "_on_FileButton_pressed", [field])


func _get_item_list(item_list: ItemList) -> PoolStringArray:
	var list = PoolStringArray()
	
	for item in item_list.items:
		if item is String:
			list.append(item)
			
	return list

