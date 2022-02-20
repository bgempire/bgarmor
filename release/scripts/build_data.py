import os
import zlib
import glob
import base64
from pathlib import Path
from time import time
from fnmatch import fnmatchcase
from math import ceil
import common

data = common.getData()

COMPRESSION_LEVEL = 1
FILE_MAX_SIZE = 1024 * 1024 * 32 # bytes > KB > MB
ITEM_SEPARATOR = "\t"

def compressDataFile(sourcePath, dataFile):
    startTime = time()
    
    if dataFile.exists():
        dataFile.unlink()
    
    print("\n> Compressing data file to", dataFile.as_posix())
    
    with open(dataFile.as_posix(), "ab") as dataFileObj:
        
        for _file in glob.glob(sourcePath.as_posix() + "/**", recursive=True):
            _file = Path(_file).resolve()
            ignore = False
            
            if "Ignore" in data.keys():
                for pattern in data["Ignore"]:
                    if fnmatchcase(_file.name, pattern):
                        ignore = True
                        if _file.is_file(): print("    - Ignored", _file.relative_to(sourcePath))
                        break
            
            if _file.is_file() and not ignore and not "desktop.ini" in _file.as_posix():
                relativePath = _file.relative_to(sourcePath)
                fileSize = os.path.getsize(_file.as_posix())
                numChunks = numChunks = ceil(fileSize / FILE_MAX_SIZE) if fileSize > FILE_MAX_SIZE else 1
                curChunk = 0
                
                dataFileObj.write(base64.b64encode((relativePath.as_posix() + ITEM_SEPARATOR + str(numChunks)).encode()))
                dataFileObj.write("\n".encode())
                
                print("    > Writing", relativePath.as_posix())
                
                with open(_file.as_posix(), "rb") as currentFileObj:
                    while curChunk < numChunks:
                        dataFileObj.write(base64.b64encode(zlib.compress(currentFileObj.read(FILE_MAX_SIZE), COMPRESSION_LEVEL)))
                        dataFileObj.write("\n".encode())
                        if numChunks > 1:
                            print("        > Written chunk", curChunk + 1)
                        curChunk += 1
                    
    print("> Done! Time taken:", round(time() - startTime, 3), "seconds")

if data is not None:
    
    if "DataChunkSize" in data.keys():
        FILE_MAX_SIZE = 1024 * 1024 * data["DataChunkSize"]
    
    compressDataFile(
        data["CurPath"] / data["DataSource"],
        data["CurPath"] / data["DataFile"]
    )
