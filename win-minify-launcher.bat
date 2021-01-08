echo off
cls

echo ---------------------------------
echo BGArmor Script Minifier - Windows
echo ---------------------------------
echo.
echo This utility will minify and obfuscate the launcher.py script. You can 
echo keep any of those scripts on the launcher folder.
echo.

call ".\source\tools\Windows\get-python.bat"

if exist %PYTHON_EXECUTABLE% (
    goto RunPyminifier
) else (
    goto Finish
)

:RunPyminifier
%PYTHON_EXECUTABLE% -m source.tools.Common.pyminifier -o ./launcher/launcher.py --replacement-length=48 --obfuscate-classes --obfuscate-functions --obfuscate-import-methods --obfuscate-builtins ./source/launcher.py

:Finish
echo.
echo Done!
pause
