#!/bin/bash
echo "----------------------------------"
echo "BGArmor Executable Builder - Linux"
echo "----------------------------------"
echo

source './source/tools/Linux/get-python.sh'

if [ ! -z $PYTHON_EXECUTABLE ]; then
    $PYTHON_EXECUTABLE './source/tools/Common/helper_scripts/build_launcher.py'
    rm -f Launcher.o
fi

echo
echo "Done!"
read -p "Press any key to continue..."
