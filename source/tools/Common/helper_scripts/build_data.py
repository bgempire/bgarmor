import os
import platform
import subprocess
import zlib
import shutil
import glob
import base64
from pathlib import Path
from ast import literal_eval
from pprint import pprint
from time import time
import common

COMPRESSION_LEVEL = 1

def compressDataFile(sourcePath, dataFile):
    startTime = time()
    
    if dataFile.exists():
        dataFile.unlink()
    
    print("\n> Compressing data file to", dataFile.as_posix())
    
    with open(dataFile.as_posix(), "ab") as dataFileObj:
        for _file in glob.glob(sourcePath.as_posix() + "/**", recursive=True):
            _file = Path(_file).resolve()
            if _file.is_file() and not "__pycache__" in _file.as_posix():
                relativePath = _file.relative_to(sourcePath)
                dataFileObj.write(base64.b64encode(relativePath.as_posix().encode()))
                dataFileObj.write("\n".encode())
                with open(_file.as_posix(), "rb") as currentFileObj:
                    dataFileObj.write(base64.b64encode(zlib.compress(currentFileObj.read(), COMPRESSION_LEVEL)))
                    dataFileObj.write("\n".encode())
                    print("    > Written", relativePath.as_posix())
                    
    print("> Done! Time taken:", round(time() - startTime, 3), "seconds")

data = common.getData()

if data is not None:
    compressDataFile(
        data["CurPath"] / data["DataSource"],
        data["CurPath"] / data["DataFile"]
    )
