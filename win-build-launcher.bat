echo off
cls

echo ------------------------------------
echo BGArmor Executable Builder - Windows
echo ------------------------------------
echo.
echo This script will build the launcher executable from the C source code. 
echo NOTE: You need the GNU GCC compiler (MinGW) in order to build the launcher.
echo.

REM Get Python executable path from current platform configuration
set /p PYTHON_EXECUTABLE=<.\launcher\Windows\python_executable.txt

REM Format path variable resolve
set PYTHON_EXECUTABLE=set %PYTHON_EXECUTABLE%

REM Resolve path variable
%PYTHON_EXECUTABLE%

REM Execute script using given Python executable
%PYTHON_EXECUTABLE% ".\source\tools\Common\helper_scripts\build_launcher.py"

echo.
echo Done!

pause
