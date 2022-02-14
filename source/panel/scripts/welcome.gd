extends Control

onready var globals = $"/root/Globals"

func _ready() -> void:
	pass


func _on_ButtonNew_pressed() -> void:
	$FileDialogNew.show()


func _on_ButtonDocs_pressed() -> void:
	OS.shell_open("https://github.com/bgempire/bgarmor/wiki")


func _on_ButtonSource_pressed() -> void:
	OS.shell_open("https://github.com/bgempire/bgarmor")
