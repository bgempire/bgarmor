#!/bin/bash
echo "----------------------------------"
echo "BGArmor Executable Builder - Linux"
echo "----------------------------------"
echo

# Get Python executable path from current platform configuration
PYTHON_EXECUTABLE=$(cat ./launcher/Linux/python_executable.txt)

# Resolve path variable
eval $PYTHON_EXECUTABLE

# Execute script using given Python executable
$PYTHON_EXECUTABLE './source/tools/Common/helper_scripts/build_launcher.py'

rm -f Launcher.o

echo "Done!"
read -p "Press any key to continue..."
