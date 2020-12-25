echo off
cls

echo ------------------------------------
echo BGArmor Engine Icon Setter - Windows
echo ------------------------------------
echo.
echo This utility will change the icon of the engine executable according to 
echo the path provided by ./launcher/Windows/engine_executable.txt to the 
echo icon ./source/icons/icon-engine.ico

REM Get engine executable path from current platform configuration
set /p ENGINE_EXECUTABLE=<.\launcher\Windows\engine_executable.txt

REM Format path variable resolve
set ENGINE_EXECUTABLE=set %ENGINE_EXECUTABLE%

REM Resolve path variable
%ENGINE_EXECUTABLE%

REM Format set icon command for rcedit
set INPUT_COMMAND=".\source\tools\Windows\rcedit.exe" --set-icon ".\source\icons\icon-engine.ico" %ENGINE_EXECUTABLE%

echo.
echo Setting engine icon...
echo Command: %INPUT_COMMAND%
%INPUT_COMMAND%

echo.
echo Done!

pause
