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

REM Get Python executable path from current platform configuration
set /p PYTHON_EXECUTABLE=<.\launcher\Windows\python_executable.txt

REM Format path variable resolve
set PYTHON_EXECUTABLE=set %PYTHON_EXECUTABLE%

REM Resolve path variable
%PYTHON_EXECUTABLE%

REM Execute script using given Python executable
%PYTHON_EXECUTABLE% ".\source\tools\Common\helper_scripts\set_icons.py"

echo.
echo Done!

pause
