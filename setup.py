from __future__ import annotations
import sys
from cx_Freeze import Executable, setup

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Tells the build script to hide the console.

executables = [Executable("main.py", base=base, icon='static/ico/icon.ico', target_name="DotaOPDSG.exe")]

setup(
    name="DotaOPDSG",
    options={'build_exe': {'include_files': ['static', 'version.txt']}},
    executables=executables,
)
