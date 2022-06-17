import common as _common
from pathlib import Path as _Path


ITEM_SEPARATOR = "\t"

data = _common.getProjectData()


def main():
    # type: () -> None

    print("Started game package data build")

    if data:
        _compressDataFile(data, data["CurPath"] / data["DataSource"], data["CurPath"] / data["DataFile"])


def _compressDataFile(data, sourcePath, dataFile):
    # type: (dict[str, object], _Path, _Path) -> None

    import os
    import zlib
    import glob
    import base64
    from time import time
    from fnmatch import fnmatchcase
    from math import ceil

    compressionLevel = int(data.get("CompressionLevel", 1))
    chunkMaxSize = 1024 * 1024 * int(data.get("DataChunkSize", 32))
    compileScripts = data.get("CompileScripts", False) # type: bool

    startTime = time()

    if dataFile.exists():
        dataFile.unlink()

    if compileScripts:
        print("> Compiling Python scripts at:", sourcePath.as_posix())
        __compileScripts(sourcePath)

    print("> Compressing data file to", dataFile.as_posix())

    with open(dataFile.as_posix(), "ab") as dataFileObj:

        for _file in glob.glob(sourcePath.as_posix() + "/**", recursive=True):
            _file = _Path(_file).resolve()
            ignore = False
            isIgnoredScript = _file.suffix == ".py" and compileScripts
            isCompiledScript = _file.suffix == ".pyc" and compileScripts

            if not isCompiledScript and "Ignore" in data.keys():
                pathToMatch = _file.as_posix().replace(sourcePath.as_posix(), "")

                for pattern in data["Ignore"]:
                    if isIgnoredScript or fnmatchcase(pathToMatch, pattern):
                        ignore = True
                        if _file.is_file():
                            print("    - Ignored", _file.relative_to(sourcePath))
                        break

            if _file.is_file() and not ignore:
                relativePath = _file.relative_to(sourcePath)
                fileSize = os.path.getsize(_file.as_posix())
                numChunks = ceil(fileSize / chunkMaxSize) if fileSize > chunkMaxSize else 1
                curChunk = 0

                dataFileObj.write(base64.b64encode((relativePath.as_posix() + ITEM_SEPARATOR + str(numChunks)).encode()))
                dataFileObj.write("\n".encode())

                print("    > Writing", relativePath.as_posix())

                with open(_file.as_posix(), "rb") as currentFileObj:
                    while curChunk < numChunks:
                        dataFileObj.write(base64.b64encode(zlib.compress(currentFileObj.read(chunkMaxSize), compressionLevel)))
                        dataFileObj.write("\n".encode())
                        if numChunks > 1:
                            print("        > Written chunk", curChunk + 1)
                        curChunk += 1

    if compileScripts:
        _removeCompiledScripts(sourcePath)

    print("> Done! Time taken:", round(time() - startTime, 3), "seconds")


def __compileScripts(directory):
    # type: (_Path) -> None

    import compileall
    import shutil
    import os
    import sys
    from pathlib import Path

    pycSuffix = ".cpython-{}{}".format(sys.version_info.major, sys.version_info.minor)

    compileall.compile_dir(directory.as_posix(), quiet=1, force=True)

    # Move .pyc files out of __pycache__
    for path, dirs, files in os.walk(directory.as_posix()):
        for file in files:
            _file = Path(path) / file # type: Path

            if _file.suffix == ".pyc":
                if _file.parent.name == "__pycache__" and pycSuffix in _file.name:
                    _file.rename(_file.parent.parent / _file.name.replace(pycSuffix, ""))
                else:
                    _file.unlink()

    # Remove __pycache__ folders
    for path, dirs, files in os.walk(directory.as_posix()):
        _path = Path(path)

        if _path.name == "__pycache__":
            shutil.rmtree(_path.as_posix())


def _removeCompiledScripts(directory):
    # type: (_Path) -> None

    import os

    for path, dirs, files in os.walk(directory.as_posix()):
        for file in files:
            _file = _Path(path) / file # type: _Path

            if _file.suffix == ".pyc":
                _file.unlink()


try:
    main()
except Exception as e:
    print(e)
