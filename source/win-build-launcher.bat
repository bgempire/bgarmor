echo off
cls

echo -----------------------------
echo BGLauncher Executable Builder
echo -----------------------------
echo.

REM Get launcher name from user
set /P LAUNCHER_PATH="Name of the launcher (optional, example: My Game): "

REM Set default name if no name is provided by user
if "%LAUNCHER_PATH%"=="" set LAUNCHER_PATH=Launcher

REM Add the quotes and extension to launcher name
set LAUNCHER_PATH="..\%LAUNCHER_PATH%.exe"

REM Format compile command for tcc
set INPUT_COMMAND=".\tools\Windows\tcc.exe" -o %LAUNCHER_PATH% ".\launcher.c"

echo.
echo Building launcher...
echo Command: %INPUT_COMMAND%
%INPUT_COMMAND%

REM Format set icon command for rcedit
set INPUT_COMMAND=".\tools\Windows\rcedit.exe" --set-icon ".\icon-launcher.ico" %LAUNCHER_PATH%

echo.
echo Setting launcher icon...
echo Command: %INPUT_COMMAND%
%INPUT_COMMAND%

echo.
echo Done!

pause