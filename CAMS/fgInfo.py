import ctypes
from .mvlib import MvFgLib
from . import fgHeaders as fgh
from .errors import get_err
import logging
from .Utils import structure_to_dict


def getIfInfo(i):
    ifinfo = fgh.MV_FG_INTERFACE_INFO()
    ret = MvFgLib.MV_FG_GetInterfaceInfo(ctypes.c_uint(i), ctypes.byref(ifinfo))
    info = {}
    if ret != 0:
        logging.error('Интерфес №', i, get_err(ret, 1))
        return
    if ifinfo.nTLayerType == fgh.MV_FG_CXP_INTERFACE:
        info['Type'] = 'CXP_INTERFACE'
        info.update(structure_to_dict(ifinfo.IfaceInfo.stCXPIfaceInfo))
    elif ifinfo.nTLayerType == fgh.MV_FG_GEV_INTERFACE:
        info['Type'] = 'GEV_INTERFACE'
        info.update(structure_to_dict(ifinfo.IfaceInfo.stGEVIfaceInfo))
    elif ifinfo.nTLayerType == fgh.MV_FG_CAMERALINK_INTERFACE:
        info['Type'] = 'CAMERALINK_INTERFACE'
        info.update(structure_to_dict(ifinfo. IfaceInfo.stCMLIfaceInfo))
    elif ifinfo.nTLayerType == fgh.MV_FG_XoF_INTERFACE:
        info['Type'] = 'XoF_INTERFACE'
        info.update(structure_to_dict(ifinfo.IfaceInfo.stXoFIfaceInfo))
    return info


def getIfaces():
    x = ctypes.c_bool()
    ret = MvFgLib.MV_FG_UpdateInterfaceList(0xffff, ctypes.byref(x))
    if ret:
        logging.error('Не удалось получить интерфейсы ' + get_err(ret, 1))
        return
    nInterfaceNum = ctypes.c_uint(0)
    out = []
    ret = MvFgLib.MV_FG_GetNumInterfaces(ctypes.byref(nInterfaceNum))
    if ret:
        logging.error('Не удалось получить интерфейсы ' + get_err(ret, 1))
        return
    for i in range(nInterfaceNum.value):
        out.append(getIfInfo(i))
    return out


def getDevs(hInterface):
    out = []
    x = ctypes.c_bool()
    ret = MvFgLib.MV_FG_UpdateDeviceList(hInterface, ctypes.byref(x))
    if ret:
        logging.error('MV_FG_UpdateDeviceList ' + get_err(ret))
        return
    nDeviceNum = ctypes.c_uint()
    ret = MvFgLib.MV_FG_GetNumDevices(hInterface, ctypes.byref(nDeviceNum))
    if ret:
        logging.error('MV_FG_GetNumDevices '+get_err(ret))
        return
    for i in range(nDeviceNum.value):
        out.append(getDevInfo(hInterface, i))
    return out


def getDevInfo(hInterface, i):
    info = {}
    stDeviceInfo = fgh.MV_FG_DEVICE_INFO()
    ret = MvFgLib.MV_FG_GetDeviceInfo(hInterface, ctypes.c_uint(i), ctypes.byref(stDeviceInfo))
    if ret != 0:
        logging.error('Камера № '+str(i)+' '+get_err(ret, 1))
        return
    if stDeviceInfo.nDevType == fgh.MV_FG_CXP_DEVICE:
        info['Type'] = ('CXP_DEVICE')
        info.update(structure_to_dict(stDeviceInfo.DevInfo.stCXPDevInfo))
    elif stDeviceInfo.nDevType == fgh.MV_FG_GEV_DEVICE:
        info['Type'] = ('GEV_DEVICE')
        info.update(structure_to_dict(stDeviceInfo.DevInfo.stGEVDevInfo))
    if stDeviceInfo.nDevType == fgh.MV_FG_CAMERALINK_DEVICE:
        info['Type'] = ('CAMERALINK_DEVICE')
        info.update(structure_to_dict(stDeviceInfo.DevInfo.stCMLDevInfo))
    elif stDeviceInfo.nDevType == fgh.MV_FG_XoF_DEVICE:
        info['Type'] = ('XoF_DEVICE')
        info.update(structure_to_dict(stDeviceInfo.DevInfo.stXoFDevInfo))
    return info
