echo off
cls

echo ------------------------------
echo BGArmor Data Builder - Windows
echo ------------------------------
echo.
echo This script will compress the game source code and will obey all
echo the settings  provided by ./launcher/config.json
echo.

call ".\source\tools\Windows\get-python.bat" ".\source\tools\Common\helper_scripts\build_data.py"

echo.
echo Done!
pause