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
        data["EngineExecutables"] = []
        
        with open(configFile.as_posix(), 'r') as sourceFile:
            data.update(literal_eval(sourceFile.read()))
            print("> Read config from", configFile.as_posix())
            
        engineFiles = [p / "engine_executable.txt" for p in (curPath / "launcher").iterdir() if ("Windows" in p.name or "Linux" in p.name) and p.is_dir()]
        
        for engineFile in engineFiles:
            if engineFile.exists():
                with open(engineFile.as_posix(), 'r') as sourceFile:
                    engineExecutable = Path(sourceFile.read().split('=')[-1].replace('"', "").replace("'", "").replace("\n", ""))
                    if engineExecutable.exists():
                        data["EngineExecutables"].append(engineExecutable.resolve())
                
    return data

def formatFileName(name, spaces=True, lowercase=False):
    allowedChars = string.ascii_lowercase + string.digits + ".-"
    result = ""
    
    if spaces:
        allowedChars += " "
    elif not spaces:
        name = name.replace(" ", "-")
        
    if lowercase:
        name = name.lower()
    elif not lowercase:
        allowedChars += string.ascii_uppercase
        
    for c in name:
        if c in allowedChars:
            result += c
    return result
