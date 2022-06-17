class_name BGArmorGlobals
extends Node


const MAX_RECENT_PROJECTS = 5
const DEFAULT_CONFIG: Dictionary = {
	"LastDir": "",
	"RecentPaths": [],
}

const DEFAULT_PLATFORMS: PoolStringArray = PoolStringArray([
	"Windows32",
	"Windows64",
	"Linux32",
	"Linux64",
])

const DEFAULT_PROJECT_FOLDERS: PoolStringArray = PoolStringArray([
	"",
	"data",
	"engine",
	"engine/Linux32",
	"engine/Linux64",
	"engine/Windows32",
	"engine/Windows64",
	"launcher",
	"icons",
])

const DEFAULT_PROJECT_FILES: PoolStringArray = PoolStringArray([
	"data/Example Game.blend",
	"icons/icon-engine.ico",
	"icons/icon-launcher.ico",
	"launcher/Launcher.exe",
	"launcher/Launcher",
	"launcher/launcher.py",
])

const DEFAULT_FIELDS: Dictionary = {
	"GameName": "Game",
	"Version": "0.0.1",
	"BGArmorVersion": 0,
	"MainFile": "Example Game.blend",
	"DataFile": "./data.dat",
	"DataSource": "./data",
	"DataChunkSize": 32,
	"CompressionLevel": 1,
	"CompileScripts": false,
	"ExportCompress": false,
	"EngineWindows32": "./engine/Windows32/blenderplayer.exe",
	"EngineWindows64": "./engine/Windows64/blenderplayer.exe",
	"EngineLinux32": "./engine/Linux32/blenderplayer",
	"EngineLinux64": "./engine/Linux64/blenderplayer",
	"PythonWindows32": "./engine/Windows32/2.79/python/bin/python.exe",
	"PythonWindows64": "./engine/Windows64/2.79/python/bin/python.exe",
	"PythonLinux32": "./engine/Linux32/2.79/python/bin/python3.5m",
	"PythonLinux64": "./engine/Linux64/2.79/python/bin/python3.5m",
	"Persistent": [
		"*.bgeconf",
	],
	"Ignore": [
		"*.pyc",
		"*.blend1"
	]
}

onready var current_project_path: String = ""
onready var current_project_dir: String = ""
onready var current_project_data: Dictionary = {}
onready var config: Dictionary = {}


func _ready() -> void:
	load_config()


func load_config():
	var config_path = OS.get_user_data_dir() + "/config.json"
	var config_file = File.new()
	
	if config_file.open(config_path, File.READ) == OK:
		config = JSON.parse(config_file.get_as_text()).result
		print("Loaded config from", config_path)
		
	else:
		config = JSON.parse(JSON.print(DEFAULT_CONFIG)).result
		save_config()
	
	config_file.close()


func save_config():
	var config_path = OS.get_user_data_dir() + "/config.json"
	var config_file = File.new()
	
	if config_file.open(config_path, File.WRITE) == OK:
		
		if config_file.file_exists(config_path):
			config_file.store_string(JSON.print(config))
			print("Saved config to " + config_path)
			
		else:
			config_file.store_string(JSON.print(DEFAULT_CONFIG))
			print("Created new config in " + config_path)
			
	else:
		print("Could not create config file at " + config_path)


func add_project_to_recent(path: String):
	var recent_paths: Array = config.get("RecentPaths", [])
	
	if recent_paths.has(path):
		recent_paths.remove(recent_paths.find(path))
		
	recent_paths.push_front(path)
	
	if recent_paths.size() > MAX_RECENT_PROJECTS:
		recent_paths.resize(MAX_RECENT_PROJECTS)
		
	config["RecentPaths"] = recent_paths


func save_project():
	
	if current_project_path:
		var file = File.new()
		
		if file.open(current_project_path, File.WRITE) == OK:
			file.store_string(JSON.print(current_project_data))
			
		file.close()
		print("Project saved to: " + current_project_path)


func get_json_no_comments(json: String) -> String:
	var lines = json.split("\n")
	var finalJson = ""
	
	for line in lines:
		line = line.strip_edges()
		
		if not line.begins_with("//"):
			finalJson += line
			
	return finalJson


func find_by_class(node: Node, _class_name: String, result: Array = []) -> Array:
	if node.is_class(_class_name) :
		result.push_back(node)

	for child in node.get_children():
		var _temp = find_by_class(child, _class_name, result)
		
	return result


func get_path_parent(path: String) -> String:
	var path_array = path.split("/")
	
	if path_array.size():
		path_array.resize(path_array.size() - 2)
		
	path = path_array.join("/")
	return path
