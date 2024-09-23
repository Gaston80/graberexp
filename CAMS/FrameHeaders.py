import ctypes
from .mvlib import sysName

if sysName == 'Win':
    PixelType = ctypes.c_int
else:
    PixelType = ctypes.c_int64


class MV_CHUNK_DATA_CONTENT(ctypes.Structure):
    _fields_ = [
        ('pChunkData', ctypes.POINTER(ctypes.c_ubyte)),
        ('nChunkID', ctypes.c_uint),
        ('nChunkLen', ctypes.c_uint),
        ('nReserved', ctypes.c_uint * 8)]


class N22_MV_FRAME_OUT_INFO_EX_3DOT_1E(ctypes.Union):
    _fields_ = [
        ('pUnparsedChunkContent', ctypes.POINTER(MV_CHUNK_DATA_CONTENT)),
        ('nAligning', ctypes.c_int64)]


class MV_FRAME_OUT_INFO_EX(ctypes.Structure):
    _fields_ = [
        ('nWidth', ctypes.c_ushort),
        ('nHeight', ctypes.c_ushort),
        ('enPixelType', PixelType),
        ('nFrameNum', ctypes.c_uint),
        ('nDevTimeStampHigh', ctypes.c_uint),
        ('nDevTimeStampLow', ctypes.c_uint),
        ('nReserved0', ctypes.c_uint),
        ('nHostTimeStamp', ctypes.c_int64),
        ('nFrameLen', ctypes.c_uint),
        ('nSecondCount', ctypes.c_uint),
        ('nCycleCount', ctypes.c_uint),
        ('nCycleOffset', ctypes.c_uint),
        ('fGain', ctypes.c_float),
        ('fExposureTime', ctypes.c_float),
        ('nAverageBrightness', ctypes.c_uint),
        ('nRed', ctypes.c_uint),
        ('nGreen', ctypes.c_uint),
        ('nBlue', ctypes.c_uint),
        ('nFrameCounter', ctypes.c_uint),
        ('nTriggerIndex', ctypes.c_uint),
        ('nInput', ctypes.c_uint),
        ('nOutput', ctypes.c_uint),
        ('nOffsetX', ctypes.c_ushort),
        ('nOffsetY', ctypes.c_ushort),
        ('nChunkWidth', ctypes.c_ushort),
        ('nChunkHeight', ctypes.c_ushort),
        ('nLostPacket', ctypes.c_uint),
        ('nUnparsedChunkNum', ctypes.c_uint),
        ('UnparsedChunkList', N22_MV_FRAME_OUT_INFO_EX_3DOT_1E),
        ('nReserved', ctypes.c_uint * 36),
    ]


class MV_FRAME_OUT(ctypes.Structure):
    _fields_ = [
        ('pBufAddr', ctypes.POINTER(ctypes.c_ubyte)),
        ('stFrameInfo', MV_FRAME_OUT_INFO_EX),
        ('nRes', ctypes.c_uint * 16)]


c_frame = MV_FRAME_OUT
c_frameInfo = MV_FRAME_OUT_INFO_EX
