echo off
cls

echo ------------------------------
echo BGArmor Data Builder - Windows
echo ------------------------------
echo.
echo This script will compress the game source code with the provided 
echo password at ./source/metadata.txt and will obey all the settings 
echo provided by ./launcher/config.json
echo.

REM Get Python executable path from current platform configuration
set /p PYTHON_EXECUTABLE=<.\launcher\Windows\python_executable.txt

REM Format path variable resolve
set PYTHON_EXECUTABLE=set %PYTHON_EXECUTABLE%

REM Resolve path variable
%PYTHON_EXECUTABLE%

REM Execute script using given Python executable
%PYTHON_EXECUTABLE% ".\source\tools\Common\helper_scripts\build_data.py"

echo.
echo Done!
pause