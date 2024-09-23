import ctypes

MV_FG_MAX_IF_INFO_SIZE = 64
MV_FG_MAX_SYMBOLIC_NUM = 64
MV_FG_MAX_SYMBOLIC_STRLEN = 64
MV_FG_GEV_DEVICE = 0x00000001
MV_FG_U3V_DEVICE = 0x00000002
MV_FG_CAMERALINK_DEVICE = 0x00000003
MV_FG_CXP_DEVICE = 0x00000004
MV_FG_XoF_DEVICE = 0x00000005
MV_FG_MAX_DEV_INFO_SIZE = 64
MV_FG_GEV_INTERFACE = 0x00000001
MV_FG_U3V_INTERFACE = 0x00000002
MV_FG_CAMERALINK_INTERFACE = 0x00000004
MV_FG_CXP_INTERFACE = 0x00000008
MV_FG_XoF_INTERFACE = 0x00000010
MV_FG_MAX_IF_INFO_SIZE = 64

MV_FG_PIXEL_TYPE = ctypes.c_uint32


class MV_CML_INTERFACE_INFO(ctypes.Structure):
    _fields_ = [
        ("chInterfaceID", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),      # Идентификатор интерфейса
        ("chDisplayName", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),      # Отображаемое имя
        ("chSerialNumber", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),     # Серийный номер
        ("nPCIEInfo", ctypes.c_uint),                                   # Информация о разъеме PCIe интерфейса
        ("chModelName", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),         # Наименование модели
        ("chManufacturer", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),      # Наименование производителя
        ("chDeviceVersion", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),     # Версия устройства
        ("chUserDefinedName", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE)    # Пользовательское определенное имя
    ]


class MV_CXP_INTERFACE_INFO(ctypes.Structure):
    _fields_ = [
        ("chInterfaceID", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),      # Идентификатор интерфейса
        ("chDisplayName", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),      # Отображаемое имя
        ("chSerialNumber", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),     # Серийный номер
        ("nPCIEInfo", ctypes.c_uint),                                   # Информация о разъеме PCIe интерфейса
        ("chModelName", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),         # Наименование модели
        ("chManufacturer", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),      # Наименование производителя
        ("chDeviceVersion", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),     # Версия устройства
        ("chUserDefinedName", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE)    # Пользовательское определенное имя
    ]


class MV_GEV_INTERFACE_INFO(ctypes.Structure):
    _fields_ = [
        ("chInterfaceID", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),
        ("chDisplayName", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),
        ("chSerialNumber", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),
        ("nPCIEInfo", ctypes.c_uint),
        ("chModelName", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),
        ("chManufacturer", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),
        ("chDeviceVersion", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),
        ("chUserDefinedName", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE)
    ]


class MV_XoF_INTERFACE_INFO(ctypes.Structure):
    _fields_ = [
        ("chInterfaceID", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),      # Идентификатор интерфейса
        ("chDisplayName", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),      # Отображаемое имя
        ("chSerialNumber", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),     # Серийный номер
        ("nPCIEInfo", ctypes.c_uint),                                   # Информация о разъеме PCIe интерфейса
        ("chModelName", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),         # Наименование модели
        ("chManufacturer", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),      # Наименование производителя
        ("chDeviceVersion", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE),     # Версия устройства
        ("chUserDefinedName", ctypes.c_char * MV_FG_MAX_IF_INFO_SIZE)    # Пользовательское определенное имя
    ]


class IfUnion(ctypes.Union):
    _fields_ = [
        ("stCXPIfaceInfo", MV_CXP_INTERFACE_INFO),  # Информация о интерфейсе CoaXPress
        ("stGEVIfaceInfo", MV_GEV_INTERFACE_INFO),  # Информация о интерфейсе GigE Vision
        ("stCMLIfaceInfo", MV_CML_INTERFACE_INFO),  # Информация о интерфейсе Camera Link
        ("stXoFIfaceInfo", MV_XoF_INTERFACE_INFO),  # Информация о интерфейсе XoFLink
        ("nReserved", ctypes.c_uint * 256)           # Зарезервировано
    ]


class MV_FG_INTERFACE_INFO(ctypes.Structure):
    _fields_ = [
        ("nTLayerType", ctypes.c_uint),            # Тип интерфейса
        ("nReserved", ctypes.c_uint * 4),          # Зарезервировано
        ("IfaceInfo", IfUnion)                       # Информация об интерфейсе
    ]


class MV_CXP_DEVICE_INFO(ctypes.Structure):
    _fields_ = [
        ("chVendorName", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),      # Название производителя
        ("chModelName", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),       # Название модели
        ("chManufacturerInfo", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),  # Информация о производителе
        ("chDeviceVersion", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),   # Версия устройства
        ("chSerialNumber", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),    # Серийный номер
        ("chUserDefinedName", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),  # Пользовательское определенное имя
        ("chDeviceID", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),        # Идентификатор устройства
        ("nReserved", ctypes.c_uint * 48)                              # Зарезервировано
    ]


class MV_GEV_DEVICE_INFO(ctypes.Structure):
    _fields_ = [
        ("nIpCfgOption", ctypes.c_uint),            # Опции конфигурации IP
        ("nIpCfgCurrent", ctypes.c_uint),           # Текущая конфигурация IP
        ("nCurrentIp", ctypes.c_uint),              # Текущий IP-адрес
        ("nCurrentSubNetMask", ctypes.c_uint),      # Текущая маска подсети
        ("nDefultGateWay", ctypes.c_uint),          # Текущий шлюз по умолчанию
        ("nNetExport", ctypes.c_uint),              # Экспорт сети
        ("nMacAddress", ctypes.c_uint64),           # MAC-адрес
        ("chVendorName", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),      # Название производителя
        ("chModelName", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),       # Название модели
        ("chManufacturerInfo", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),  # Информация о производителе
        ("chDeviceVersion", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),   # Версия устройства
        ("chSerialNumber", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),    # Серийный номер
        ("chUserDefinedName", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),  # Пользовательское определенное имя
        ("chDeviceID", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),        # Идентификатор устройства
        ("nCurrentPort", ctypes.c_uint),            # Текущий порт
        ("nReserved", ctypes.c_uint * 47)           # Зарезервировано
    ]


class MV_CML_DEVICE_INFO(ctypes.Structure):
    _fields_ = [
        ("chVendorName", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),
        ("chModelName", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),
        ("chManufacturerInfo", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),
        ("chDeviceVersion", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),
        ("chSerialNumber", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),
        ("chUserDefinedName", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),
        ("chDeviceID", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),
        ("nReserved", ctypes.c_uint * 48)
    ]


class MV_XoF_DEVICE_INFO(ctypes.Structure):
    _fields_ = [
        ("chVendorName", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),
        ("chModelName", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),
        ("chManufacturerInfo", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),
        ("chDeviceVersion", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),
        ("chSerialNumber", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),
        ("chUserDefinedName", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),
        ("chDeviceID", ctypes.c_char * MV_FG_MAX_DEV_INFO_SIZE),
        ("nReserved", ctypes.c_uint * 48)
    ]


class DevUnion(ctypes.Union):
    _fields_ = [
        ("stCXPDevInfo", MV_CXP_DEVICE_INFO),  # Информация о интерфейсе CoaXPress
        ("stGEVDevInfo", MV_GEV_DEVICE_INFO),  # Информация о интерфейсе GigE Vision
        ("stCMLDevInfo", MV_CML_DEVICE_INFO),  # Информация о интерфейсе Camera Link
        ("stXoFDevInfo", MV_XoF_DEVICE_INFO),  # Информация о интерфейсе XoFLink
        ("nReserved", ctypes.c_uint * 256)           # Зарезервировано
    ]


class MV_FG_DEVICE_INFO(ctypes.Structure):
    _fields_ = [
        ("nDevType", ctypes.c_uint),
        ("nReserved", ctypes.c_uint * 3),
        ("DevInfo", DevUnion)  # Замените на соответствующий тип данных
    ]


class MV_FG_BUFFER_INFO(ctypes.Structure):
    _fields_ = [
        ("pBuffer", ctypes.POINTER(ctypes.c_ubyte)),
        ("nSize", ctypes.c_uint),
        ("nFilledSize", ctypes.c_uint),
        ("pPrivate", ctypes.c_void_p),
        ("nWidth", ctypes.c_uint),
        ("nHeight", ctypes.c_uint),
        ("enPixelType", MV_FG_PIXEL_TYPE),
        ("bNewData", ctypes.c_bool),
        ("bQueued", ctypes.c_bool),
        ("bAcquiring", ctypes.c_bool),
        ("bIncomplete", ctypes.c_bool),
        ("nFrameID", ctypes.c_int64),
        ("nDevTimeStamp", ctypes.c_int64),
        ("nHostTimeStamp", ctypes.c_int64),
        ("nNumChunks", ctypes.c_uint),
        ("nChunkPayloadSize", ctypes.c_uint),
        ("nSecondCount", ctypes.c_uint),
        ("nCycleCount", ctypes.c_uint),
        ("nCycleOffset", ctypes.c_uint),
        ("fGain", ctypes.c_float),
        ("fExposureTime", ctypes.c_float),
        ("nAverageBrightness", ctypes.c_uint),
        ("nFrameCounter", ctypes.c_uint),
        ("nTriggerIndex", ctypes.c_uint),
        ("nInput", ctypes.c_uint),
        ("nOutput", ctypes.c_uint),
        ("nRed", ctypes.c_uint),
        ("nGreen", ctypes.c_uint),
        ("nBlue", ctypes.c_uint),
        ("nOffsetX", ctypes.c_uint),
        ("nOffsetY", ctypes.c_uint),
        ("nChunkWidth", ctypes.c_uint),
        ("nChunkHeight", ctypes.c_uint),
        ("nLastFrameFlag", ctypes.c_uint),
        ("nReserved", ctypes.c_uint * 44),
    ]


class MV_FG_CHUNK_DATA_INFO(ctypes.Structure):
    _fields_ = [
        ("pChunkData", ctypes.POINTER(ctypes.c_ubyte)),
        ("nChunkID", ctypes.c_uint),
        ("nChunkLen", ctypes.c_uint),
        ("nReserved", ctypes.c_uint * 4),
    ]


class MV_FG_INPUT_IMAGE_INFO(ctypes.Structure):
    _fields_ = [
        ("nWidth", ctypes.c_uint),
        ("nHeight", ctypes.c_uint),
        ("enPixelType", MV_FG_PIXEL_TYPE),
        ("pImageBuf", ctypes.POINTER(ctypes.c_ubyte)),
        ("nImageBufLen", ctypes.c_uint),
        ("nReserved", ctypes.c_uint * 4),
    ]


class MV_FG_OUTPUT_IMAGE_INFO(ctypes.Structure):
    _fields_ = [
        ("nWidth", ctypes.c_uint),
        ("nHeight", ctypes.c_uint),
        ("enPixelType", MV_FG_PIXEL_TYPE),
        ("pImageBuf", ctypes.POINTER(ctypes.c_ubyte)),
        ("nImageBufSize", ctypes.c_uint),
        ("nImageBufLen", ctypes.c_uint),
        ("nReserved", ctypes.c_uint * 4),
    ]


class MV_FG_FRAME_SPEC_INFO(ctypes.Structure):
    _fields_ = [
        ("nSecondCount", ctypes.c_uint),
        ("nCycleCount", ctypes.c_uint),
        ("nCycleOffset", ctypes.c_uint),
        ("fGain", ctypes.c_float),
        ("fExposureTime", ctypes.c_float),
        ("nAverageBrightness", ctypes.c_uint),
        ("nRed", ctypes.c_uint),
        ("nGreen", ctypes.c_uint),
        ("nBlue", ctypes.c_uint),
        ("nFrameCounter", ctypes.c_uint),
        ("nTriggerIndex", ctypes.c_uint),
        ("nInput", ctypes.c_uint),
        ("nOutput", ctypes.c_uint),
        ("nOffsetX", ctypes.c_ushort),
        ("nOffsetY", ctypes.c_ushort),
        ("nFrameWidth", ctypes.c_ushort),
        ("nFrameHeight", ctypes.c_ushort),
        ("nReserved", ctypes.c_uint * 16),
    ]


class MV_FG_INTVALUE(ctypes.Structure):
    _fields_ = [
        ("nCurValue", ctypes.c_int64),
        ("nMax", ctypes.c_int64),
        ("nMin", ctypes.c_int64),
        ("nInc", ctypes.c_int64),
        ("nReserved", ctypes.c_uint * 16)
    ]


class MV_FG_ENUMVALUE(ctypes.Structure):
    _fields_ = [
        ("nCurValue", ctypes.c_uint),
        ("strCurSymbolic", ctypes.c_char * MV_FG_MAX_SYMBOLIC_STRLEN),
        ("nSupportedNum", ctypes.c_uint),
        ("nSupportValue", ctypes.c_uint * MV_FG_MAX_SYMBOLIC_NUM),
        ("strSymbolic", (ctypes.c_char * MV_FG_MAX_SYMBOLIC_STRLEN) * MV_FG_MAX_SYMBOLIC_NUM),
        ("nReserved", ctypes.c_uint * 4)
    ]


class MV_FG_FLOATVALUE(ctypes.Structure):
    _fields_ = [
        ("fCurValue", ctypes.c_float),
        ("fMax", ctypes.c_float),
        ("fMin", ctypes.c_float),
        ("nReserved", ctypes.c_uint * 4)
    ]


class MV_FG_STRINGVALUE(ctypes.Structure):
    _fields_ = [
        ("strCurValue", ctypes.c_char * 256),
        ("nMaxLength", ctypes.c_int64),
        ("nReserved", ctypes.c_uint * 4)
    ]


class MV_FG_FILE_ACCESS(ctypes.Structure):
    _fields_ = [
        ("pUserFileName", ctypes.c_char_p),
        ("pDevFileName", ctypes.c_char_p),
        ("nReserved", ctypes.c_uint * 32)
    ]
