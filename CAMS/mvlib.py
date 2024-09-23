import ctypes
import sys

if sys.platform[0:3] == 'win':
    sysName = 'Win'
    MvLib = ctypes.cdll.LoadLibrary("C:/Program Files (x86)/Common Files/MVS/Runtime/Win64_x64/MvCameraControl.dll")
    MvFgLib = ctypes.cdll.LoadLibrary("C:/Program Files (x86)/Common Files/MVS/Runtime/Win64_x64/MVFGControl.dll")
else:
    sysName = 'linux'
    MvLib = ctypes.cdll.LoadLibrary("/opt/MVS/lib/64/libMvCameraControl.so")
    MvFgLib = ctypes.cdll.LoadLibrary("/opt/MVS/lib/64/libMVFGControl.so")
# C:/Program Files (x86)/Common Files/MVS/Runtime/Win64_x64/MvCameraControl.dll
# c:\Program Files (x86)\Common Files\MVS\Runtime\Win32_i86\MvCameraControl.dll
