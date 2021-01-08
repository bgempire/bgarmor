REM Tries to get the Python executable from several game engine paths
REM After the executable is found, executes it if an argument is given, exits if not

set DEBUG_SCRIPT=0
set PATH_ROOT=.\launcher\
set PATH_FILE=\python_executable.txt

:GetWindows32Python
if %DEBUG_SCRIPT%==1 echo GetWindows32Python
set WIN_VERSION=Windows32
if exist %PATH_ROOT%%WIN_VERSION%%PATH_FILE% (
    set /p PYTHON_EXECUTABLE=<%PATH_ROOT%%WIN_VERSION%%PATH_FILE%
    goto ResolvePathVariable
) else (
    goto GetWindows64Python
)

:GetWindows64Python
if %DEBUG_SCRIPT%==1 echo GetWindows64Python
set WIN_VERSION=Windows64
if exist %PATH_ROOT%%WIN_VERSION%%PATH_FILE% (
    set /p PYTHON_EXECUTABLE=<%PATH_ROOT%%WIN_VERSION%%PATH_FILE%
    goto ResolvePathVariable
) else (
    goto GetWindowsPython
)

:GetWindowsPython
if %DEBUG_SCRIPT%==1 echo GetWindowsPython
set WIN_VERSION=Windows
if exist %PATH_ROOT%%WIN_VERSION%%PATH_FILE% (
    set /p PYTHON_EXECUTABLE=<%PATH_ROOT%%WIN_VERSION%%PATH_FILE%
    goto ResolvePathVariable
) else (
    goto PythonNotFound
)

:ResolvePathVariable
if %DEBUG_SCRIPT%==1 echo ResolvePathVariable
set PYTHON_EXECUTABLE=set %PYTHON_EXECUTABLE%
%PYTHON_EXECUTABLE%
if exist %PYTHON_EXECUTABLE% (
    goto CheckArgument
) else (
    goto PythonNotFound
)

:CheckArgument
if "%~1" == "" (
    goto EndOfScript
) else (
    goto ExecuteScript
)

:ExecuteScript
if %DEBUG_SCRIPT%==1 echo ExecuteScript
%PYTHON_EXECUTABLE% %1
goto EndOfScript

:PythonNotFound
echo X Python executable not found!
if %DEBUG_SCRIPT%==1 echo PythonNotFound

:EndOfScript
if %DEBUG_SCRIPT%==1 echo EndOfScript