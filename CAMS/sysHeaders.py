import ctypes
import logging
from .mvlib import MvLib
from . import Utils
from .errors import get_err

MV_GIGE_DEVICE = 0x00000001
MV_USB_DEVICE = 0x00000004
MV_GENTL_CAMERALINK_DEVICE = 0x00000008
MV_GENTL_CXP_DEVICE = 0x00000100
MV_GENTL_XOF_DEVICE = 0x00000200


class MV_GIGE_DEVICE_INFO(ctypes.Structure):
    _fields_ = [
        ('nIpCfgOption', ctypes.c_uint),
        ('nIpCfgCurrent', ctypes.c_uint),
        ('nCurrentIp', ctypes.c_uint),
        ('nCurrentSubNetMask', ctypes.c_uint),
        ('nDefultGateWay', ctypes.c_uint),
        ('chManufacturerName', ctypes.c_char * 32),
        ('chModelName', ctypes.c_char * 32),
        ('chDeviceVersion', ctypes.c_char * 32),
        ('chManufacturerSpecificInfo', ctypes.c_char * 48),
        ('chSerialNumber', ctypes.c_char * 16),
        ('chUserDefinedName', ctypes.c_char * 16),
        ('nNetExport', ctypes.c_uint),
        ('nReserved', ctypes.c_uint * 4)]


class MV_USB3_DEVICE_INFO(ctypes.Structure):
    _fields_ = [
        ('CrtlInEndPoint', ctypes.c_char),
        ('CrtlOutEndPoint', ctypes.c_char),
        ('StreamEndPoint', ctypes.c_char),
        ('EventEndPoint', ctypes.c_char),
        ('idVendor', ctypes.c_ushort),
        ('idProduct', ctypes.c_ushort),
        ('nDeviceNumber', ctypes.c_uint),
        ('chDeviceGUID', ctypes.c_char * 64),
        ('chVendorName', ctypes.c_char * 64),
        ('chModelName', ctypes.c_char * 64),
        ('chFamilyName', ctypes.c_char * 64),
        ('chDeviceVersion', ctypes.c_char * 64),
        ('chManufacturerName', ctypes.c_char * 64),
        ('chSerialNumber', ctypes.c_char * 64),
        ('chUserDefinedName', ctypes.c_char * 64),
        ('nbcdUSB', ctypes.c_uint),
        ('nDeviceAddress', ctypes.c_uint),
        ('nReserved', ctypes.c_uint * 2)]


class MV_CML_DEVICE_INFO(ctypes.Structure):
    _fields_ = [
        ('chInterfaceID', ctypes.c_char * 64),
        ('chVendorName', ctypes.c_char * 64),
        ('chModelName', ctypes.c_char * 64),
        ('chManufacturerName', ctypes.c_char * 64),
        ('chDeviceVersion', ctypes.c_char * 64),
        ('chSerialNumber', ctypes.c_char * 64),
        ('chUserDefinedName', ctypes.c_char * 64),
        ('chDeviceID ', ctypes.c_char * 64),
        ('nReserved', ctypes.c_uint * 7)]


class MV_CXP_DEVICE_INFO(ctypes.Structure):
    _fields_ = [
        ('chInterfaceID', ctypes.c_char * 64),
        ('chVendorName', ctypes.c_char * 64),
        ('chModelName', ctypes.c_char * 64),
        ('chManufacturerName', ctypes.c_char * 64),
        ('chDeviceVersion', ctypes.c_char * 64),
        ('chSerialNumber', ctypes.c_char * 64),
        ('chUserDefinedName', ctypes.c_char * 64),
        ('chDeviceID ', ctypes.c_char * 64),
        ('nReserved', ctypes.c_uint * 7)]


class MV_XOF_DEVICE_INFO(ctypes.Structure):
    _fields_ = [
        ('chInterfaceID', ctypes.c_char * 64),
        ('chVendorName', ctypes.c_char * 64),
        ('chModelName', ctypes.c_char * 64),
        ('chManufacturerName', ctypes.c_char * 64),
        ('chDeviceVersion', ctypes.c_char * 64),
        ('chSerialNumber', ctypes.c_char * 64),
        ('chUserDefinedName', ctypes.c_char * 64),
        ('chDeviceID ', ctypes.c_char * 64),
        ('nReserved', ctypes.c_uint * 7)]


class MV_CamL_DEV_INFO(ctypes.Structure):
    _fields_ = [
        ('chPortID', ctypes.c_char * 64),
        ('chModelName', ctypes.c_char * 64),
        ('chFamilyName', ctypes.c_char * 64),
        ('chDeviceVersion', ctypes.c_char * 64),
        ('chManufacturerName', ctypes.c_char * 64),
        ('chSerialNumber', ctypes.c_char * 64),
        ('nReserved', ctypes.c_uint * 38)]


class N19_MV_CC_DEVICE_INFO_3DOT_0E(ctypes.Union):
    _fields_ = [
        ('stGigEInfo', MV_GIGE_DEVICE_INFO),
        ('stUsb3VInfo', MV_USB3_DEVICE_INFO),
        ('stCamLInfo', MV_CamL_DEV_INFO),
        ('stCMLInfo',  MV_CML_DEVICE_INFO),
        ('stCXPInfo',   MV_CXP_DEVICE_INFO),
        ('stXoFInfo', MV_CXP_DEVICE_INFO),
        ]


class MV_CC_DEVICE_INFO(ctypes.Structure):
    _fields_ = [
        ('nMajorVer', ctypes.c_ushort),
        ('nMinorVer', ctypes.c_ushort),
        ('nMacAddrHigh', ctypes.c_uint),
        ('nMacAddrLow', ctypes.c_uint),
        ('nTLayerType', ctypes.c_uint),
        ('nReserved', ctypes.c_uint * 4),
        ('SpecialInfo', N19_MV_CC_DEVICE_INFO_3DOT_0E)]


class MV_CC_DEVICE_INFO_LIST(ctypes.Structure):
    _fields_ = [
        ('nDeviceNum', ctypes.c_uint),
        ('pDeviceInfo', ctypes.POINTER(MV_CC_DEVICE_INFO) * 256)]


class MV_GENTL_IF_INFO(ctypes.Structure):
    _fields_ = [
        ('chInterfaceID', ctypes.c_char * 64),
        ('chTLType', ctypes.c_char * 64),
        ('chDisplayName', ctypes.c_char * 64),
        ('nCtiIndex', ctypes.c_uint),
        ('nReserved', ctypes.c_uint * 8)]


class MV_GENTL_IF_INFO_LIST(ctypes.Structure):
    _fields_ = [
        ('nInterfaceNum', ctypes.c_uint),
        ('pIFInfo', ctypes.POINTER(MV_GENTL_IF_INFO) * 256)]


class MV_GENTL_DEV_INFO(ctypes.Structure):
    _fields_ = [
        ('chInterfaceID', ctypes.c_char * 64),
        ('chDeviceID', ctypes.c_char * 64),
        ('chVendorName', ctypes.c_char * 64),
        ('chModelName', ctypes.c_char * 64),
        ('chTLType', ctypes.c_char * 64),
        ('chDisplayName', ctypes.c_char * 64),
        ('chUserDefinedName', ctypes.c_char * 64),
        ('chSerialNumber', ctypes.c_char * 64),
        ('chDeviceVersion', ctypes.c_char * 64),
        ('nCtiIndex', ctypes.c_uint),
        ('nReserved', ctypes.c_uint * 8)]


class MV_GENTL_DEV_INFO_LIST(ctypes.Structure):
    _fields_ = [
        ('nDeviceNum', ctypes.c_uint),
        ('pDeviceInfo', ctypes.POINTER(MV_GENTL_DEV_INFO) * 256)]


class MV_INTERFACE_INFO (ctypes.Structure):
    _fields_ = [
        ('nTLayerType', ctypes.c_uint),
        ('nPCIEInfo', ctypes.c_uint),
        ('chDisplayName', ctypes.c_char * 64),
        ('chSerialNumber', ctypes.c_char * 64),
        ('chModelName', ctypes.c_char * 64),
        ('chManufacturer', ctypes.c_char * 64),
        ('chDeviceVersion', ctypes.c_char * 64),
        ('chUserDefinedName ', ctypes.c_char * 64),
        ('nReserved', ctypes.c_uint * 64),
        ]


class MV_INTERFACE_INFO_LIST(ctypes.Structure):
    _fields_ = [
        ('nInterfaceNum', ctypes.c_uint),
        ('pInterfaceInfos', ctypes.POINTER(MV_INTERFACE_INFO) * 64),
        ]


def getGigEDevices(Key=''):
    devs = []
    deviceList = MV_CC_DEVICE_INFO_LIST()
    ret = MvLib.MV_CC_EnumDevices(0xffff, ctypes.byref(deviceList))
    if ret != 0:
        print(get_err(ret, 1))
    for i in range(deviceList.nDeviceNum):
        dev = deviceList.pDeviceInfo[i]
        if Utils.getInfo(dev).get('Key', 'x') == Key:
            return dev
        devs.append(dev)
    if not Key:
        return devs


def getDevices(Key=''):
    devs = []
    deviceList = MV_CC_DEVICE_INFO_LIST()
    ret = MvLib.MV_CC_EnumDevices(0xffff, ctypes.byref(deviceList))
    if ret != 0:
        logging.error('MV_CC_EnumDevices '+get_err(ret, 1))
    for i in range(deviceList.nDeviceNum):
        dev = deviceList.pDeviceInfo[i]
        if Utils.getInfo(dev).get('Key', 'x') == Key:
            return dev
        devs.append(dev)
    if Key == '':
        print(Key, devs)
        return devs


path = b'/opt/MVS/lib/64/MvFGProducerCXP.cti'


def getGentlDevices():
    interfaces = MV_GENTL_IF_INFO_LIST()
    ret = MvLib.MV_CC_EnumInterfacesByGenTL(ctypes.byref(interfaces), path)
    print(ret)
    devs = []
    deviceList = MV_GENTL_DEV_INFO_LIST()
    ret = MvLib.MV_CC_EnumDevicesByGenTL()
    if ret != 0:
        # print(ret)
        pass
    for i in range(deviceList.nDeviceNum):
        dev = deviceList.pDeviceInfo[i]
        devs.append(dev)


def get_device_info(pst_mv_dev_info):
    device_info = {}

    if pst_mv_dev_info is None:
        return device_info

    if pst_mv_dev_info.nTLayerType == MV_GIGE_DEVICE:
        device_info["Type"] = 'GigE'
        dev = pst_mv_dev_info.SpecialInfo.stGigEInfo

    elif pst_mv_dev_info.nTLayerType == MV_USB_DEVICE:
        device_info["Type"] = 'USB'
        dev = pst_mv_dev_info.SpecialInfo.stUsb3VInfo
    elif pst_mv_dev_info.nTLayerType == MV_GENTL_CAMERALINK_DEVICE:
        device_info["Type"] = 'CAMERALINK'
        dev = pst_mv_dev_info.SpecialInfo.stCMLInfo
    elif pst_mv_dev_info.nTLayerType == MV_GENTL_CXP_DEVICE:
        device_info["Type"] = 'GENTL_CXP'
        dev = pst_mv_dev_info.SpecialInfo.stCXPInfo
    elif pst_mv_dev_info.nTLayerType == MV_GENTL_XOF_DEVICE:
        device_info["Type"] = 'GENTL_XOF'
        dev = pst_mv_dev_info.SpecialInfo.stXoFInfo
    device_info["chUserDefinedName"] = Utils.tostr(dev.chUserDefinedName)
    device_info["chSerialNumber"] = Utils.tostr(dev.chSerialNumber)
    device_info["chModelName"] = Utils.tostr(dev.chModelName)
    for k, v in device_info.items():
        print(k, v)

    return device_info
