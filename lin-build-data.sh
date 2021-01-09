#!/bin/bash
echo "----------------------------"
echo "BGArmor Data Builder - Linux"
echo "----------------------------"
echo
echo "This script will compress the game source code and will obey "
echo "all the settings provided by ./launcher/config.json"
echo

source './source/tools/Linux/get-python.sh'

if [ ! -z $PYTHON_EXECUTABLE ]; then
    $PYTHON_EXECUTABLE './source/tools/Common/helper_scripts/build_data.py'
fi

echo
echo "Done!"
read -p "Press any key to continue..."
