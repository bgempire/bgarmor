echo off
cls

echo ------------------------------
echo BGArmor Data Builder - Windows
echo ------------------------------
echo.

REM Get data source directory from user
set /P DATA_SOURCE="Path of the data source directory (optional, default: ..\data): "

REM Set default source directory if nothing is provided by user
if "%DATA_SOURCE%"=="" set DATA_SOURCE=..\data

REM Add quotes and wildcard to data source directory
set DATA_SOURCE="%DATA_SOURCE%\*"

REM Get data archive name from user
set /P DATA_PATH="Name of the data file (optional, default: data.dat): "

REM Set default name if no name is provided by user
if "%DATA_PATH%"=="" set DATA_PATH=data.dat

REM Add the quotes and complete data path
set DATA_PATH="..\%DATA_PATH%"

REM Get data file password from metadata.txt
set /p PASSWORD=<metadata.txt

REM Format compress command
set INPUT_COMMAND=".\tools\Windows\7za.exe" a -tzip %DATA_PATH% -p%PASSWORD% %DATA_SOURCE%

echo.
echo Building data...
echo Command: %INPUT_COMMAND%
%INPUT_COMMAND%

echo.
echo Done!

pause
