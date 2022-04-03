from pathlib import Path as _Path
from json import loads as _loads


def getArgs():
    # type: () -> dict[str, str]
    
    from sys import argv
    
    args = {}  # type: dict[str, str]
    
    for i in range(len(argv)):
        if i > 0:
            arg = argv[i]
            argNext = argv[i + 1] if len(argv) > i + 1 else True
            
            if arg.startswith("-"):
                args[arg] = argNext
                
    return args


def getProjectData(projectFile=None):
    # type: (str | _Path) -> dict[str]
    
    import platform
    from ast import literal_eval
    
    args = getArgs()
    
    if not projectFile and args.get("--project"):
        projectFile = str(args.get("--project"))
        
    data = {}  # type: dict[str, object]
    projectFile = _Path(projectFile).resolve() if type(projectFile) == str else _Path(str(projectFile))  # type: _Path
    
    if projectFile.exists():
        curPath = projectFile.parent.parent
        
        with open(projectFile.as_posix(), "r") as sourceFile:
            fileParsed = False
            
            try:
                data = _loads(sourceFile.read())
                fileParsed = True
            except:
                try:
                    data.update(literal_eval(sourceFile.read()))
                    fileParsed = True
                except:
                    print("X Could not parse project file")
                    return data
                    
            if fileParsed:
                print("> Read project from", projectFile.as_posix())
            
        engineExecutables = {}  # type: dict[str, _Path]
        
        for key in data.keys():
            if "Engine" in key:
                engineExecutable = curPath / data[key]  # type: _Path
                
                if engineExecutable.exists():
                    engineExecutables[engineExecutable.parent.name] = engineExecutable.resolve()
                        
        data["ProjectFile"] = projectFile
        data["CurPath"] = curPath
        data["Quote"] = '"' if platform.system() == "Windows" else "'"
        data["EngineExecutables"] = engineExecutables
        
    else:
        print("X Could not get project data")
    
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

