import os
import platform
import subprocess
import zlib
import shutil
from pathlib import Path
from ast import literal_eval
from pprint import pprint
from time import time
import common

startTime = time()

data = common.getData()

if data is not None:
    
    print("> Compressing zip from", data["DataSource"], "...")
    shutil.make_archive(data["DataFile"], "zip", data["DataSource"])
    
    tempFile = Path(data["DataFile"] + ".zip")
    
    with open(tempFile.as_posix(), "rb") as sourceFile:
        with open(data["DataFile"], "wb") as targetFile:
            print("\n> Writing compressed file to: ", targetFile.name, "...")
            targetFile.write(zlib.compress(sourceFile.read(), 2))
            
    if tempFile.exists():
        tempFile.unlink()
        
    endTime = time()
    print("Time taken:", endTime - startTime, "seconds")
