import sys
import os
from typing import Optional, Any

# Get Python Version
pythonVersion = str.format(str(sys.version_info.major) + str(sys.version_info.minor))
if pythonVersion == '39': pythonVersion = '38'

# Try to find the library in the './libs' directory 
__dirname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'libs')

sys.path.append(__dirname)
dirFileList = os.listdir(__dirname)
NITLibrary = None

if sys.platform == "win32":
    extension = ".pyd"
else:
    extension = ".so"

for file in dirFileList:
    if file.startswith("NITLibrary_") and file.endswith(
        str.format("_py" + pythonVersion + extension)
    ):
        print(file)
        NITLibrary = __import__(file.split(extension)[0])
        break

if NITLibrary is None:
    if sys.platform == "win32":
        print(
            (
                "NITLibrary file missing, make sure NITLibrary_x64_xxx_py"
                + pythonVersion
                + ".pyd and NITLibrary_x64.dll files are available in the 'libs' directory"
                " and that your python version (" + pythonVersion + ") is supported. "
            )
        )
    else:
        print(
            (
                "NITLibrary file missing, make sure NITLibrary_x64_xxx_py"
                + pythonVersion
                + ".so or NITLibrary_aarch64_xxx_py"
                + pythonVersion
                + ".so and NITLibrary package are correctly installed"
                " and that your python version (" + pythonVersion + ") is supported. "
            )
        )
    sys.exit()
