echo off
cls

echo -------------------------
echo BGArmor Builder - Windows
echo -------------------------
echo.
echo This script will create the release of current version of BGArmor. This is 
echo only used to create the official releases of BGArmor.
echo.

call ".\source\tools\Windows\get-python.bat" ".\source\tools\Common\helper_scripts\build_bgarmor.py"

echo.
echo Done!
pause
