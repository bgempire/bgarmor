echo off
cls

echo ---------------------------------
echo BGArmor Script Minifier - Windows
echo ---------------------------------
echo.
echo This utility will minify and obfuscate the launcher.py script. You can 
echo keep any of those scripts on the launcher folder.
echo.

REM Get Python executable path from current platform configuration
set /p PYTHON_EXECUTABLE=<.\launcher\Windows\python_executable.txt

REM Format path variable resolve
set PYTHON_EXECUTABLE=set %PYTHON_EXECUTABLE%

REM Resolve path variable
%PYTHON_EXECUTABLE%

set PYTHON_EXECUTABLE=%CD%%PYTHON_EXECUTABLE%

REM Execute script using given Python executable
set PYMINIFIER=%PYTHON_EXECUTABLE% -m source.tools.Common.pyminifier 

%PYMINIFIER% -o ./launcher/launcher.py --replacement-length=48 --obfuscate-classes --obfuscate-functions --obfuscate-import-methods --obfuscate-builtins ./source/launcher.py

echo Done!
pause
