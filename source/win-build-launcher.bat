echo off
cls

echo ---------------------------------------
echo BGLauncher Executable Builder - Windows
echo ---------------------------------------
echo.

REM Get launcher name from user
set /P LAUNCHER_PATH="Name of the launcher (optional, default: Launcher): "

REM Set default name if no name is provided by user
if "%LAUNCHER_PATH%"=="" set LAUNCHER_PATH=Launcher

REM Add the quotes and extension to launcher name
set LAUNCHER_PATH="..\%LAUNCHER_PATH%.exe"

REM Format compile command
set INPUT_COMMAND=gcc -no-pie -o %LAUNCHER_PATH% ".\Launcher.c"

echo.
echo Building launcher...
echo Command: %INPUT_COMMAND%
%INPUT_COMMAND%

REM Format set icon command for rcedit
set INPUT_COMMAND=".\tools\Windows\rcedit.exe" --set-icon ".\icons\icon-launcher.ico" %LAUNCHER_PATH%

echo.
echo Setting launcher icon...
echo Command: %INPUT_COMMAND%
%INPUT_COMMAND%

echo.
echo Done!

pause
