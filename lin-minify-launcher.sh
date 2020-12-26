#!/bin/bash
echo "---------------------------------"
echo "BGArmor Script Minifier - Windows"
echo "---------------------------------"
echo
echo "This utility will minify and obfuscate the launcher.py script. You can "
echo "keep any of those scripts on the launcher folder."
echo

# Get Python executable path from current platform configuration
PYTHON_EXECUTABLE=$(cat ./launcher/Linux/python_executable.txt)

# Resolve path variable
eval $PYTHON_EXECUTABLE

# Execute script using given Python executable
PYMINIFIER="$PYTHON_EXECUTABLE -m source.tools.Common.pyminifier"

$PYMINIFIER -o './launcher/launcher.py' --replacement-length=48 --obfuscate-classes --obfuscate-functions --obfuscate-import-methods --obfuscate-builtins './source/launcher.py'

echo
echo Done!
read -p "Press any key to continue..."
