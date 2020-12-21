echo off
cls

echo ---------------------------------------
echo BGLauncher Engine Icon Setter - Windows
echo ---------------------------------------
echo.
echo This utility will change the icon of ./engine/Windows/blenderplayer.exe with the icon ./source/icons/icon-engine.ico.

REM Get engine executable name from user
set /P ENGINE_EXE="Name of the engine executable (optional, default: blenderplayer.exe): "

REM Set default name if no name is provided by user
if "%ENGINE_EXE%"=="" set ENGINE_EXE=blenderplayer.exe

REM Format set icon command for rcedit
set INPUT_COMMAND=".\tools\Windows\rcedit.exe" --set-icon ".\icons\icon-engine.ico" "..\engine\Windows\%ENGINE_EXE%"

echo.
echo Setting engine icon...
echo Command: %INPUT_COMMAND%
%INPUT_COMMAND%

echo.
echo Done!

pause
