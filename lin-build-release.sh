#!/bin/bash
echo "---------------------------------"
echo "BGArmor Release Builder - Windows"
echo "---------------------------------"
echo
echo "This script will generate builds for the selected available  "
echo "platforms. These releases can be compressed as well."
echo

source './source/tools/Linux/get-python.sh'

if [ ! -z $PYTHON_EXECUTABLE ]; then
    read -p "Build compressed game data? (y/n) " ANSWER
    if [ $ANSWER == 'y' ]; then
        source './lin-build-data.sh'
    elif [ $ANSWER == 'Y' ]; then
        source './lin-build-data.sh'
    fi
    $PYTHON_EXECUTABLE './source/tools/Common/helper_scripts/build_release.py'
fi

echo
echo "Done!"
read -p "Press any key to continue..."
