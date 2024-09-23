import ctypes


class MVCC_ENUMVALUE_T(ctypes.Structure):
    _fields_ = [
        ('nCurValue', ctypes.c_uint),
        ('nSupportedNum', ctypes.c_uint),
        ('nSupportValue', ctypes.c_uint * 64),
        ('nReserved', ctypes.c_uint * 4)]


class MVCC_INTVALUE_T(ctypes.Structure):
    _fields_ = [
        ('nCurValue', ctypes.c_uint),
        ('nMax', ctypes.c_uint),
        ('nMin', ctypes.c_uint),
        ('nInc', ctypes.c_uint),
        ('nReserved', ctypes.c_uint * 4)]


class MVCC_INTVALUE_EX_T(ctypes.Structure):
    _fields_ = [
        ('nCurValue', ctypes.c_int64),
        ('nMax', ctypes.c_int64),
        ('nMin', ctypes.c_int64),
        ('nInc', ctypes.c_int64),
        ('nReserved', ctypes.c_uint * 16)]


class MVCC_FLOATVALUE_T(ctypes.Structure):
    _fields_ = [
        ('fCurValue', ctypes.c_float),
        ('fMax', ctypes.c_float),
        ('fMin', ctypes.c_float),
        ('nReserved', ctypes.c_uint * 4)]


class MVCC_STRINGVALUE_T(ctypes.Structure):
    _fields_ = [
        ('chCurValue', ctypes.c_char * 256),
        ('nMaxLength', ctypes.c_int64),
        ('nReserved', ctypes.c_uint * 2)]


class MVCC_ENUMENTRY(ctypes.Structure):
    _fields_ = [
        ('nCurValue', ctypes.c_uint),
        ('chSymbolic', ctypes.c_char * 64),
        ('nReserved', ctypes.c_uint * 4)]


class MV_XML_NODE_FEATURE(ctypes.Structure):
    _fields_ = [
        ("enType", ctypes.c_uint),
        ("enVisivility", ctypes.c_uint),
        ("strDescription", ctypes.c_char * 512),
        ("strDisplayName", ctypes.c_char * 64),
        ("strName", ctypes.c_char * 64),
        ("strToolTip", ctypes.c_char * 512),
        ("nReserved", ctypes.c_uint * 4)
    ]


class MV_XML_NODES_LIST(ctypes.Structure):
    _fields_ = [
        ("nNodeNum", ctypes.c_uint),
        ("stNodes", MV_XML_NODE_FEATURE * 128)
    ]


NodeTypes = ['Value', 'Base', 'Int', 'Bool', 'Cmd', 'Float', 'Str', 'Reg', 'Cat', 'Enum', 'EnumE', 'Port']
