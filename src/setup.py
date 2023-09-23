from cx_Freeze import setup, Executable
import sys

build_exe_options = {"includes": ["os", "PIL", "cv2", "face_recognition"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="guifoo",
    version="0.1",
    description="My GUI application!",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/main.py", base=base)],
)
