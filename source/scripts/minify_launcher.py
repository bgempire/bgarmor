import zlib
import base64
import subprocess
import sys

from pathlib import Path

pythonExecutable = Path(sys.executable).resolve()
rootPath = Path(__file__).parent.parent.parent
launcherPathSource = rootPath / "source/launcher.py"
launcherPathTarget = rootPath / "release/launcher/launcher.py"

# Minify to release directory using pyminifier
args = [
    pythonExecutable.as_posix(), "-m", "source.scripts.pyminifier", 
    "-o", launcherPathTarget.as_posix(), 
    "--replacement-length=48", 
    "--obfuscate-classes", 
    "--obfuscate-functions", 
    "--obfuscate-import-methods", 
    "--obfuscate-builtins", 
    launcherPathSource.as_posix(),
]
print("> Minifying", launcherPathSource.as_posix(), "to", launcherPathTarget.as_posix())
subprocess.call(args)

# Encode minified source to base64 and write final launcher.py
launcherHeader = '''
from base64 import b64decode as bng34i8g349ng3948n2f
from zlib import decompress as plioknwef2n902349209n
jhfgd90i34gniorfg93n4girbng903=exec
imnv34908inv34908v2349m0g4="""'''

launcherFooter = '''"""
jhfgd90i34gniorfg93n4girbng903(plioknwef2n902349209n(bng34i8g349ng3948n2f(imnv34908inv34908v2349m0g4.encode())).decode())
'''

if launcherPathTarget.exists():
    print("> Encoding launcher script to", launcherPathTarget.as_posix())
    launcherData = None # type: str
    
    with open(launcherPathTarget.as_posix(), "r") as openedFile:
        launcherData = openedFile.read()
    
    with open(launcherPathTarget.as_posix(), "w") as openedFile:
        launcherContent = base64.b64encode(zlib.compress(launcherData.encode())).decode()
        openedFile.write(launcherHeader + launcherContent + launcherFooter)
        
    print("> Done!")
        
else:
    print("X Launcher script not found:", launcherPathTarget.as_posix())
