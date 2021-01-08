echo off
cls

echo ------------------------------------
echo BGArmor Executable Builder - Windows
echo ------------------------------------
echo.
echo This script will build the launcher executable from the C source code. 
echo NOTE: You need the GNU GCC compiler (MinGW) in order to build the launcher.
echo.

call ".\source\tools\Windows\get-python.bat" ".\source\tools\Common\helper_scripts\build_launcher.py"

echo.
echo Done!
pause
