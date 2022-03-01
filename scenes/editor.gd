extends Control

const POPUP_RATIO = 0.75
const COLOR_NORMAL = Color.white
const COLOR_INVALID = Color("ff7878")
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
		"node": "ButtonDataFile",
		"field": "DataFile",
		"property": "text",
		"ignore_missing": true,
	},
	{
		"node": "ButtonMainFile",
		"field": "MainFile",
		"property": "text",
		"ignore_missing": true,
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
const EXPORT_TARGETS := PoolStringArray([
	"All",
	"Linux32",
	"Linux64",
	"Windows32",
	"Windows64",
])

var BUTTON_FILE_DIALOG_RELATIONS = [
	{
		"node": "ButtonMainFile",
		"field": "MainFile",
		"filters": PoolStringArray(["*.blend ; Blend File"]),
		"mode": FileDialog.MODE_OPEN_FILE,
		"title": "Select the game main blend file",
		"filename_only": true,
	},
	{
		"node": "ButtonDataFile",
		"field": "DataFile",
		"filters": PoolStringArray(["*.dat ; Data File"]),
		"mode": FileDialog.MODE_SAVE_FILE,
		"title": "Select the game package data file",
	},
	{
		"node": "ButtonDataSource",
		"field": "DataSource",
		"filters": PoolStringArray(["*.* ; Data Source"]),
		"mode": FileDialog.MODE_OPEN_DIR,
		"title": "Select the game source data directory",
	},
	{
		"node": "ButtonEngineWindows32",
		"field": "EngineWindows32",
		"filters": PoolStringArray(["*.exe ; Executable"]),
		"mode": FileDialog.MODE_OPEN_FILE,
		"title": "Select the engine executable",
	},
	{
		"node": "ButtonEngineWindows64",
		"field": "EngineWindows64",
		"filters": PoolStringArray(["*.exe ; Executable"]),
		"mode": FileDialog.MODE_OPEN_FILE,
		"title": "Select the engine executable",
	},
	{
		"node": "ButtonEngineLinux32",
		"field": "EngineLinux32",
		"filters": PoolStringArray(["* ; Executable"]),
		"mode": FileDialog.MODE_OPEN_FILE,
		"title": "Select the engine executable",
	},
	{
		"node": "ButtonEngineLinux64",
		"field": "EngineLinux64",
		"filters": PoolStringArray(["* ; Executable"]),
		"mode": FileDialog.MODE_OPEN_FILE,
		"title": "Select the engine executable",
	},
	{
		"node": "ButtonPythonWindows32",
		"field": "PythonWindows32",
		"filters": PoolStringArray(["*.exe ; Executable"]),
		"mode": FileDialog.MODE_OPEN_FILE,
		"title": "Select the Python executable",
	},
	{
		"node": "ButtonPythonWindows64",
		"field": "PythonWindows64",
		"filters": PoolStringArray(["*.exe ; Executable"]),
		"mode": FileDialog.MODE_OPEN_FILE,
		"title": "Select the Python executable",
	},
	{
		"node": "ButtonPythonLinux32",
		"field": "PythonLinux32",
		"filters": PoolStringArray(["* ; Executable"]),
		"mode": FileDialog.MODE_OPEN_FILE,
		"title": "Select the Python executable",
	},
	{
		"node": "ButtonPythonLinux64",
		"field": "PythonLinux64",
		"filters": PoolStringArray(["* ; Executable"]),
		"mode": FileDialog.MODE_OPEN_FILE,
		"title": "Select the Python executable",
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
	_connect_export_buttons()
	var _error = $FileDialog.connect("dir_selected", self, "_on_FileDialog_any_selected")
	_error = $FileDialog.connect("file_selected", self, "_on_FileDialog_any_selected")


func _notification(what):
	if what == MainLoop.NOTIFICATION_WM_FOCUS_IN:
		_update_fields()


# Signal handlers
func _on_ButtonBuildData_pressed() -> void:
	_run_script("release/scripts/build_data.py", [])


func _on_ButtonSetIcons_pressed() -> void:
	_run_script("release/scripts/set_icons.py", [
		"--resource-hacker", _get_resource("release/tools/ResourceHacker.exe")
	])


func _on_ButtonExport_pressed(target: String) -> void:
	var args = ["--target", target]
	var checkbox: CheckBox = find_node("CheckBoxExportCompress")
	
	if checkbox.pressed:
		args.append("--compress")
		
	_run_script("release/scripts/build_release.py", args)


func _on_ButtonExplore_pressed() -> void:
	var _error = OS.shell_open(globals.current_project_dir)


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


func _on_SpinBoxCompressionLevel_value_changed(value: float) -> void:
	globals.current_project_data["CompressionLevel"] = int(value)


func _on_FileButton_pressed(data: Dictionary) -> void:
	var file_dialog = $FileDialog
	file_dialog.mode = data["mode"]
	file_dialog.filters = data["filters"]
	file_dialog.window_title = data["title"]
	file_dialog.current_dir = globals.current_project_dir
	file_dialog.dialog_text = data["node"]
	file_dialog.popup_centered_ratio(POPUP_RATIO)


func _on_FileDialog_any_selected(path: String) -> void:
	
	if globals.current_project_dir in path:
		var field_name = $FileDialog.dialog_text.replace("Button", "")
		var field: Dictionary = {}
		
		for _field in BUTTON_FILE_DIALOG_RELATIONS:
			if _field.get("field") == field_name:
				field = _field
				break
		
		var button: Button = find_node($FileDialog.dialog_text)
		var relative_path: String = path.replace(globals.current_project_dir, ".")
		
		if field.get("filename_only"):
			relative_path = relative_path.split("/")[-1]
		
		globals.current_project_data[field_name] = relative_path
		button.text = relative_path
		_update_fields()
		
	else:
		$AcceptDialog/TextEdit.text = "Path must be inside project folder!"
		$AcceptDialog.popup_centered_ratio(POPUP_RATIO)


# Abstraction methods
func _update_fields() -> void:
	var cur_project = globals.current_project_data
	var default = globals.DEFAULT_FIELDS
	var file_fields = PoolStringArray()
	var cur_dir: Directory = Directory.new()
	var _error = cur_dir.open(globals.current_project_dir)
	
	for field in BUTTON_FILE_DIALOG_RELATIONS:
		file_fields.append(field["field"])
	
	for field in NODE_FIELD_RELATIONS:
		var cur_node = find_node(field["node"])
		
		if cur_node:
			
			if field.get("is_item_list"):
				var item_list: ItemList = cur_node
				item_list.clear()
				
				for item in cur_project.get(field["field"], default[field["field"]]):
					item_list.add_item(item)
				
			else:
				var control: Control = cur_node
				var field_value = cur_project.get(field["field"], default[field["field"]])
				var ignore_missing: bool = field.get("ignore_missing", false)
				
				control.set(
					field["property"], 
					field_value
				)
				
				if field["field"] in file_fields:
					
					if ignore_missing or cur_dir.file_exists(field_value) or cur_dir.dir_exists(field_value):
						control.self_modulate = COLOR_NORMAL
						control.hint_tooltip = ""
						
					else:
						control.self_modulate = COLOR_INVALID
						control.hint_tooltip = "Could not find this target."
		
		else:
			print("Could not find node: " + field["node"])
			
	_update_task_buttons()


func _update_task_buttons() -> void:
	var project = globals.current_project_data
	var cur_dir: Directory = Directory.new()
	var _error = cur_dir.open(globals.current_project_dir)
	var python_valid = _get_python_current_os() and true
	
	var tooltip = "" if python_valid else "Python executable for current platform must be set first."
	
	# Set toggle tasks based on existing Python executable
	var tasks = PoolStringArray(["BuildData", "SetIcons", "ExportAll"])
	
	for task in tasks:
		var button_task: Button = find_node("Button" + task)
		button_task.disabled = not python_valid
		button_task.hint_tooltip = tooltip
	
	for platform in globals.DEFAULT_PLATFORMS:
		var button_export: Button = find_node("ButtonExport" + platform)
		var button_run: Button = find_node("ButtonRun" + platform)
		var cur_tooltip = ""
		
		if python_valid:
			
			if cur_dir.file_exists(project["Python" + platform]) and cur_dir.file_exists(project["Engine" + platform]):
				button_export.disabled = false
				button_run.disabled = false
			
			else:
				button_export.disabled = true
				button_run.disabled = true
				cur_tooltip = "Python and engine executables must be set for this platform."
			
		else:
			button_export.disabled = true
			button_run.disabled = true
			cur_tooltip = tooltip
			
		button_export.hint_tooltip = cur_tooltip
		button_run.hint_tooltip = cur_tooltip


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


func _connect_export_buttons() -> void:
	
	for target in EXPORT_TARGETS:
		var button: Button = find_node("ButtonExport" + target)
		var _error = button.connect("pressed", self, "_on_ButtonExport_pressed", [target])


func _get_item_list(item_list: ItemList) -> PoolStringArray:
	var list = PoolStringArray()
	
	for item in item_list.items:
		if item is String:
			list.append(item)
			
	return list


func _get_python_current_os() -> String:
	var cur_dir: Directory = Directory.new()
	var _error = cur_dir.open(globals.current_project_dir)
	var cur_os = "Windows" if OS.get_name() == "Windows" else "Linux"
	var result = ""
	
	if cur_dir.file_exists(globals.current_project_data["Python" + cur_os + "32"]):
		result = globals.current_project_data["Python" + cur_os + "32"]
		
	elif cur_dir.file_exists(globals.current_project_data["Python" + cur_os + "64"]):
		result = globals.current_project_data["Python" + cur_os + "64"]
		
	if result:
		result = result.replace("./", globals.current_project_dir + "/")
		
	return result


func _get_resource(path: String) -> String:
	
	if OS.has_feature("editor"):
		path = ProjectSettings.globalize_path(path)
	else:
		path = OS.get_executable_path().get_base_dir().plus_file(path)
	
	return path


func _run_script(script_path: String, script_args: Array) -> void:
	var result = []
	var args = [_get_resource(script_path), "--project", globals.current_project_path]
	args.append_array(script_args)
	var text = "Please wait, running task..."
	
	$AcceptDialog/TextEdit.text = text
	$AcceptDialog.popup_centered_ratio(POPUP_RATIO)
	yield(get_tree().create_timer(0.25), "timeout")
	var _error = OS.execute(_get_python_current_os(), args, true, result, true)
	
	if _error == OK:
		if len(result):
			text = result.pop_back()
		else:
			text = "Task completed!"
	else:
		text = "Could not execute task! Error:" + str(_error)
		
	$AcceptDialog/TextEdit.text = text
	$AcceptDialog.popup_centered_ratio(POPUP_RATIO)
