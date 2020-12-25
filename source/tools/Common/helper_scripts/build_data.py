import os
import platform
import subprocess
from pathlib import Path
from ast import literal_eval
from pprint import pprint
import common

data = common.getData()

if data is not None:
    data["DataSource"] += "/*"
    meta = "-p" + data["Meta"] + " "
    
    command = data["Quote"] + data["7za"].as_posix() + data["Quote"] + ' a -tzip '
    command += data["Quote"] + data["DataFile"] + data["Quote"] + " "
    command += meta + data["Quote"] + data["DataSource"] + data["Quote"]
    
    print("\nCommand:", command)
    os.system(command)
