from pathlib import Path as _Path


def getArgs():
    # type: () -> dict[str, str]
    
    from sys import argv
    
    args = {} # type: dict[str, str]
    
    for i in range(len(argv)):
        if i > 0:
            arg = argv[i]
            argNext = argv[i + 1] if len(argv) > i + 1 else True
            
            if arg.startswith("-"):
                args[arg] = argNext
                
    return args


def getProjectData(projectFile):
    # type: (str | _Path) -> dict[str, object]
    
    import platform
    from ast import literal_eval
    
    data = {} # type: dict[str, object]
    projectFile = _Path(projectFile).resolve() if type(projectFile) == str else projectFile.resolve() # type: _Path
    
    if projectFile.exists():
        curPath = projectFile.parent
        
        with open(projectFile.as_posix(), "r") as sourceFile:
            data.update(literal_eval(sourceFile.read()))
            print("> Read config from", projectFile.as_posix())
            
        engineExecutables = [] # type: list[_Path]
        
        for key in data.keys():
            if "Engine" in key:
                engineExecutable = curPath / data[key] # type: _Path
                
                if engineExecutable.exists:
                    engineExecutables.append(engineExecutable)
                        
        data["CurPath"] = curPath
        data["Quote"] = '"' if platform.system() == "Windows" else "'"
        data["EngineExecutables"] = engineExecutables
                
    return data


def formatFileName(name, spaces=True, lowercase=False):
    # type: (str, bool, bool) -> str
    
    import string
    
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

