import os
import platform
import subprocess
import string
from pathlib import Path
from ast import literal_eval

def getData():
    data = {}
    
    curPath = Path(__file__).parent.resolve()
    
    if curPath.name == 'helper_scripts':
        curPath = curPath.parent.parent.parent.parent
        os.chdir(curPath.as_posix())
        
    configFile = curPath / './launcher/config.json'
    
    if configFile.exists():
        data["CurPath"] = curPath
        data["Quote"] = '"' if platform.system() == "Windows" else "'"
        
        with open(configFile.as_posix(), 'r') as sourceFile:
            data.update(literal_eval(sourceFile.read()))
            print("> Read config from", configFile.as_posix())
            
        engineFile = curPath / ('./launcher/' + platform.system() + '/engine_executable.txt')
        
        if engineFile.exists():
            with open(engineFile.as_posix(), 'r') as sourceFile:
                data["EngineExecutable"] = Path(sourceFile.read().split('=')[-1].replace('"', "").replace("'", ""))
                print("> Read engine path from", engineFile.as_posix())
                
    return data

def formatFileName(name):
    result = ""
    allowedChars = string.ascii_lowercase + string.ascii_uppercase + " -"
    for c in name:
        if c in allowedChars:
            result += c
    return result
