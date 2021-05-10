import zlib
import base64

from pathlib import Path
from pprint import pprint

import common

data = common.getData()

launcherHeader = '''
from base64 import b64decode as bng34i8g349ng3948n2f
from zlib import decompress as plioknwef2n902349209n
imnv34908inv34908v2349m0g4 = """'''

launcherFooter = '''"""
exec(plioknwef2n902349209n(bng34i8g349ng3948n2f(imnv34908inv34908v2349m0g4.encode())).decode())
'''

if data is not None:
    curPath = data["CurPath"]
    launcherPath = curPath / "launcher/launcher.py"
    
    if launcherPath.exists():
        launcherData = None
        
        with open(launcherPath.as_posix(), "r") as openedFile:
            launcherData = openedFile.read()
        
        with open(launcherPath.as_posix(), "w") as openedFile:
            openedFile.write(
                launcherHeader + base64.b64encode(zlib.compress(launcherData.encode())).decode() + launcherFooter
            )
            print("> Encoded launcher script:", openedFile.name)
            
    else:
        print("X Launcher script not found:", launcherPath.as_posix())
