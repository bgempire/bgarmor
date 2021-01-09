echo off
cls

echo ---------------------------------
echo BGArmor Release Builder - Windows
echo ---------------------------------
echo.
echo This script will generate builds for the selected available 
echo platforms. These releases can be compressed as well.
echo.

set /p BUILD_DATA=Build compressed game data? (y/n) 
echo.
if %BUILD_DATA%==y goto BuildData
if %BUILD_DATA%==Y (
    goto BuildData
) else (
    goto BuildRelease
)

:BuildData
echo.
call ".\win-build-data.bat"

:BuildRelease
cls
call ".\source\tools\Windows\get-python.bat" ".\source\tools\Common\helper_scripts\build_release.py"

echo.
echo Done!
pause