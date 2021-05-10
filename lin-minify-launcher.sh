#!/bin/bash
echo "---------------------------------"
echo "BGArmor Script Minifier - Windows"
echo "---------------------------------"
echo
echo "This utility will minify and obfuscate the launcher.py script. You can "
echo "keep any of those scripts on the launcher folder."
echo

source './source/tools/Linux/get-python.sh'

if [ ! -z $PYTHON_EXECUTABLE ]; then
    PYMINIFIER="$PYTHON_EXECUTABLE -m source.tools.Common.pyminifier"
    $PYMINIFIER -o './launcher/launcher.py' --replacement-length=48 --obfuscate-classes --obfuscate-functions --obfuscate-import-methods --obfuscate-builtins './source/launcher.py'
    $PYTHON_EXECUTABLE './source/tools/Common/helper_scripts/minify_launcher.py'
fi

echo
echo Done!
read -p "Press any key to continue..."
