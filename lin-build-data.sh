#!/bin/bash
echo "----------------------------"
echo "BGArmor Data Builder - Linux"
echo "----------------------------"
echo
echo "This script will compress the game source code with the provided "
echo "password at ./source/metadata.txt and will obey all the settings "
echo "provided by ./launcher/config.json"
echo

# Get Python executable path from current platform configuration
PYTHON_EXECUTABLE=$(cat ./launcher/Linux/python_executable.txt)

# Resolve path variable
eval $PYTHON_EXECUTABLE

# Execute script using given Python executable
$PYTHON_EXECUTABLE './source/tools/Common/helper_scripts/build_data.py'

echo
echo "Done!"
read -p "Press any key to continue..."
