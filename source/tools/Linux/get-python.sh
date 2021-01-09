#!/bin/bash
readonly PATH_ROOT="./launcher/"
readonly PATH_FILE="/python_executable.txt"
readonly AVAILABLE_VERSIONS=("Linux32" "Linux64" "Linux")
PYTHON_EXECUTABLE=''

# Loads the path from the given version txt file, if it's found
function get_python_path () {
    local full_path=$PATH_ROOT$1$PATH_FILE
    if test -f $full_path; then
        PYTHON_EXECUTABLE=$(cat $full_path)
        eval $PYTHON_EXECUTABLE
        if test -f $PYTHON_EXECUTABLE; then
            chmod +x $PYTHON_EXECUTABLE
            return 0
        else
            PYTHON_EXECUTABLE='PythonNotFound'
        fi
    else
        PYTHON_EXECUTABLE='PythonNotFound'
    fi
}

# Tries to get the Python executable from the available versions
for version in ${AVAILABLE_VERSIONS[@]}; do
    get_python_path $version
    if [ $PYTHON_EXECUTABLE != 'PythonNotFound' ]; then
        break
    fi
done

# Get Python from system path if not found in available versions
if [ $PYTHON_EXECUTABLE == 'PythonNotFound' ]; then
    PYTHON_EXECUTABLE=`which python3`
fi

# If the last command did not return any path set to not found
if [ -z $PYTHON_EXECUTABLE ]; then
    PYTHON_EXECUTABLE='PythonNotFound'
fi

# Report Python not found
if [ $PYTHON_EXECUTABLE == 'PythonNotFound' ]; then
    PYTHON_EXECUTABLE=''
    echo 'X Python executable not found!'
fi
