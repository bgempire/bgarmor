echo off
cls

echo ------------------------------------
echo BGLauncher Script Minifier - Windows
echo ------------------------------------
echo.

echo This utility will minify and obfuscate the launcher.py script. You can keep any of those scripts on the launcher folder. You need Python and pyminifier installed in order to execute this utility.

pyminifier -o ../launcher/launcher_min.py --replacement-length=48 --obfuscate-classes --obfuscate-functions --obfuscate-import-methods --obfuscate-builtins ../launcher/launcher.py

echo Done!
pause
