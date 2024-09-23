from .fgHeaders import MV_FG_ENUMVALUE, MV_FG_STRINGVALUE
from .mvlib import MvFgLib
import ctypes


def getInt(handle, Node):
    val = ctypes.c_int(0)
    ret = MvFgLib.MV_FG_GetIntValue(handle, Node.encode(), ctypes.byref(val))
    if ret:
        return
    return(val.value)


def getFloat(handle, Node):
    val = ctypes.c_float(0)
    ret = MvFgLib.MV_FG_GetFloatValue(handle, Node.encode(), ctypes.byref(val))
    if ret:
        return
    return(val.value)


def getBool(handle, Node):
    val = ctypes.c_bool(0)
    ret = MvFgLib.MV_FG_GetBoolValue(handle, Node.encode(), ctypes.byref(val))
    if ret:
        return
    return(val.value)


def getString(handle, Node):
    val = MV_FG_STRINGVALUE()
    ret = MvFgLib.MV_FG_GetStringValue(handle, Node.encode(), ctypes.byref(val))
    if ret:
        return
    return(val.strCurValue.decode())


def getEnum(handle, Node):
    val = MV_FG_ENUMVALUE()
    ret = MvFgLib.MV_FG_GetEnumValue(handle, Node.encode(), ctypes.byref(val))
    if ret:
        return
    return(val.strCurSymbolic.decode())


def setInt(handle, Node, val):
    val = int(val)
    ret = MvFgLib.MV_FG_SetIntValue(handle, Node.encode(), ctypes.c_int(val))
    if ret:
        return
    return True


def setFloat(handle, Node, val):
    val = float(val)
    ret = MvFgLib.MV_FG_SetFloatValue(handle, Node.encode(), ctypes.c_float(val))
    if ret:
        return
    return True


def setBool(handle, Node, val):
    val = bool(val)
    ret = MvFgLib.MV_FG_SetBoolValue(handle, Node.encode(), ctypes.c_bool(val))
    if ret:
        return
    return True


def setString(handle, Node, val):
    val = str(val)
    ret = MvFgLib.MV_FG_SetStringValue(handle, Node.encode(), val.encode())
    if ret:
        return
    return True


def setEnum(handle, Node, val):
    val = str(val)
    ret = MvFgLib.MV_FG_SetEnumValueByString(handle, Node.encode(), val.encode())
    if ret:
        return
    return True


def execCmd(handle, Node):
    ret = MvFgLib.MV_FG_SetCommandValue(handle, Node.encode())
    if ret:
        return
    return True


def getNodeType(handle, Node):
    val = ctypes.c_int(0)
    types = ['Value', 'Base', 'Int', 'Bool', 'Cmd', 'Float', 'Str', 'Reg', 'Cat', 'Enum', 'EnumE', 'Port']
    ret = MvFgLib.MV_FG_GetNodeInterfaceType(handle, Node.encode(), ctypes.byref(val))
    if ret:
        return
    return types[val.value]


def getNode(handle, Node):
    t = getNodeType(handle, Node)
    if t == 'Int':
        return getInt(handle, Node)
    elif t == 'Bool':
        return getBool(handle, Node)
    elif t == 'Float':
        return getFloat(handle, Node)
    elif t == 'Str':
        return getString(handle, Node)
    elif t == 'Enum':
        return getEnum(handle, Node)


def setNode(handle, Node, val):
    t = getNodeType(handle, Node)
    if t == 'Int':
        return setInt(handle, Node, val)
    elif t == 'Bool':
        return setBool(handle, Node, val)
    elif t == 'Float':
        return setFloat(handle, Node, val)
    elif t == 'Str':
        return setString(handle, Node, val)
    elif t == 'Enum':
        return setEnum(handle, Node, val)
    elif t == 'Cmd':
        return execCmd(handle, Node)


def setNodes(handle, Nodes):
    for node in Nodes:
        key, val = node[:2]
        if setNode(handle, key, val):
            print('+ Ok Установлено', key, 'в', val)
        else:
            print('- ERR Не удалось установить', key, 'в', val)
