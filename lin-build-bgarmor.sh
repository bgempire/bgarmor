#!/bin/bash
echo "-----------------------"
echo "BGArmor Builder - Linux"
echo "-----------------------"
echo "This script will create the release of current version of BGArmor. This is "
echo "only used to create the official releases of BGArmor."

source './source/tools/Linux/get-python.sh'

if [ ! -z $PYTHON_EXECUTABLE ]; then
    $PYTHON_EXECUTABLE './source/tools/Common/helper_scripts/build_bgarmor.py'
    rm -f Launcher.o
fi

echo
echo "Done!"
read -p "Press any key to continue..."
