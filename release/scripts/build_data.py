from pathlib import Path as _Path


COMPRESSION_LEVEL = 1
CHUNK_MAX_SIZE = 1024 * 1024 * 32 # bytes > KB > MB
ITEM_SEPARATOR = "\t"


def compressDataFile(data, sourcePath, dataFile):
    # type: (dict[str, object], _Path, _Path) -> None
    
    import os
    import zlib
    import glob
    import base64
    from time import time
    from fnmatch import fnmatchcase
    from math import ceil
    
    startTime = time()
    
    if dataFile.exists():
        dataFile.unlink()
    
    print("> Compressing data file to", dataFile.as_posix())
    
    with open(dataFile.as_posix(), "ab") as dataFileObj:
        
        for _file in glob.glob(sourcePath.as_posix() + "/**", recursive=True):
            _file = _Path(_file).resolve()
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
                numChunks = numChunks = ceil(fileSize / CHUNK_MAX_SIZE) if fileSize > CHUNK_MAX_SIZE else 1
                curChunk = 0
                
                dataFileObj.write(base64.b64encode((relativePath.as_posix() + ITEM_SEPARATOR + str(numChunks)).encode()))
                dataFileObj.write("\n".encode())
                
                print("    > Writing", relativePath.as_posix())
                
                with open(_file.as_posix(), "rb") as currentFileObj:
                    while curChunk < numChunks:
                        dataFileObj.write(base64.b64encode(zlib.compress(currentFileObj.read(CHUNK_MAX_SIZE), COMPRESSION_LEVEL)))
                        dataFileObj.write("\n".encode())
                        if numChunks > 1:
                            print("        > Written chunk", curChunk + 1)
                        curChunk += 1
                    
    print("> Done! Time taken:", round(time() - startTime, 3), "seconds")


def main():
    import common
    
    global CHUNK_MAX_SIZE
    data = common.getProjectData()
    
    if data:
        CHUNK_MAX_SIZE = 1024 * 1024 * int(data.get("DataChunkSize", 32))
        compressDataFile(data, data["CurPath"] / data["DataSource"], data["CurPath"] / data["DataFile"])

main()