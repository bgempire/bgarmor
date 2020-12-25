# BGArmor

## Directory: engine

This directory is used to store the BGE/UPBGE runtime. You can basically copy 
and paste the content of Blender/UPBGE installation folder into the specific 
platform.

### Needed files: Windows

Some engine files are not needed in the final release of the game, so you can
delete these files. Below there is a relation of the NEEDED files for the 
engine to run properly on Windows:

```
engine/Windows/2.XX/python/*
engine/Windows/blenderplayer.exe
engine/Windows/OpenAL32.dll
engine/Windows/OpenColorIO.dll
engine/Windows/SDL2.dll
engine/Windows/avcodec-57.dll
engine/Windows/avdevice-57.dll
engine/Windows/avformat-57.dll
engine/Windows/avutil-55.dll
engine/Windows/libsndfile-1.dll
engine/Windows/pthreadVC2.dll
engine/Windows/python35.dll
engine/Windows/swresample-2.dll
engine/Windows/swscale-4.dll
```

Although all the files inside `engine/Windows/2.XX/python/` directory are 
needed, you can safely delete the `engine/Windows/2.XX/python/lib/test/` 
directory in order to save some additional megabytes. All other files CAN be 
safely deleted (including `engine/Windows/blender.exe` executable, 
`engine/Windows/2.XX/datafiles/` and `engine/Windows/2.XX/scripts/` folders).

### Needed files: Linux

Some engine files are not needed in the final release of the game, so you can
delete these files. Below there is a relation of the NEEDED files for the 
engine to run properly on Linux:

```
engine/Linux/2.XX/python/*
engine/Linux/blenderplayer*
```