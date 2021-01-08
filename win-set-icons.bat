echo off
cls

echo ------------------------------------
echo BGArmor Engine Icon Setter - Windows
echo ------------------------------------
echo.
echo This utility will change the icon of the engine executable according to 
echo the path provided by ./launcher/Windows/engine_executable.txt to the 
echo icon ./source/icons/icon-engine.ico
echo.

call ".\source\tools\Windows\get-python.bat" ".\source\tools\Common\helper_scripts\set_icons.py"

echo.
echo Done!
pause
