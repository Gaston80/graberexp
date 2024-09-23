import struct
import ctypes
from random import randint


def strIP(IP):
    data = struct.pack('>L', IP)
    strIP = ''
    for i in range(4):
        strIP += str(data[i])+'.'
    return strIP[:-1]


def intIP(IP):
    data = IP.split('.')
    intIP = 0
    if len(data) != 4:
        return 0
    for i in range(4):
        intIP += int(data[3-i])*(0x100**i)
    return intIP


def validIP(camIP, netIP):
    return ((intIP(camIP) & 0xFFFFFF00) == (intIP(netIP) & 0xFFFFFF00))


def getValidIp(netIP):
    IP = (intIP(netIP) & 0xFFFFFF00) + randint(80, 250)
    if IP == intIP(netIP):
        IP += 1
    return strIP(IP)


def tostr(data):
    return bytes(data).decode().strip(chr(0))


def getID(N, minID):
    return (N-minID) % (0x10000-minID) + minID


ipFields = ('nCurrentIp', 'nCurrentSubNetMask', 'nDefultGateWay', 'nNetExport')


def structure_to_dict(struct):
    result = {}
    for field_name, field_type in struct._fields_:
        field_value = getattr(struct, field_name)
        # Если поле имеет тип Structure, рекурсивно вызываем функцию для преобразования его в словарь
        if isinstance(field_value, ctypes.Structure):
            field_value = structure_to_dict(field_value)
        if isinstance(field_value, bytes):
            field_value = field_value.decode()
        if field_name in ipFields:
            field_value = strIP(field_value)
        result[field_name] = field_value
        result.pop('nReserved', 0)
    return result


MV_GIGE_DEVICE = 0x00000001
MV_USB_DEVICE = 0x00000004
MV_GENTL_CAMERALINK_DEVICE = 0x00000008
MV_GENTL_CXP_DEVICE = 0x00000100
MV_GENTL_XOF_DEVICE = 0x00000200


def get_device_info(pst_mv_dev_info):
    pst_mv_dev_info = pst_mv_dev_info.contents
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
    device_info.update(structure_to_dict(dev))
    txt = 'Камера: '+device_info.get('chModelName', '-')+'\n'
    txt += 'Производитель: '+device_info.get('chManufacturerName', '-')+'\n'
    txt += 'Модель: '+device_info.get('chModelName', '-')+'\n'
    txt += 'Серийный номер: '+device_info.get('chSerialNumber', '-')+'\n'
    txt += 'Идентификатор: '+device_info.get('chUserDefinedName', '-')+'\n'
    txt += 'IP камеры: '+device_info.get('nCurrentIp', '-')+'\n'
    txt += 'IP интерфейса: '+device_info.get('nNetExport', '-')+'\n'
    txt += 'Интерфейс: '+device_info.get('chInterfaceID', '-')+'\n'
    device_info['txtInfo'] = txt
    device_info['Key'] = device_info.get('chSerialNumber', '-')
    return device_info


getInfo = get_device_info


def htmlVal(val):
    html = ''
    v = val.pop('CurrentValue', '')
    if (not str(v)) or (str(v) == 'None'):
        return ''
    t = val.get('enType', '')
    if t == 'Cmd':
        html += f': <button onclick="cmdSend(\'Exec {val["strName"]}\')">Выполнить</button>'
    elif t == 'Int' or t == 'Float' or t == 'Str':
        html += f': <input id="{val["strName"]}" value="{str(v)}" size="8">'
        html += f' <button onclick="cmdSend(\'Set {val["strName"]}\',\'{val["strName"]}\')">Установить</button>'
    elif t == 'Bool':
        ch = ''
        if str(v) == 'True':
            ch = 'checked'
        html += f': <input type="checkbox" id="{val["strName"]}" {ch}>'
        html += f' <button onclick="cmdSend(\'Set {val["strName"]}\',\'{val["strName"]}\')">Установить</button>'
    elif t == 'Enum':
        html += f': <select id="{val["strName"]}" ><option value="{str(v)}">{str(v)}</option>'
        for item in val['nSupportValue']:
            if item == str(v):
                continue
            html += f"<option value='{item}'>{item}</option>"
        html += f'</select> <button onclick="cmdSend(\'Set {val["strName"]}\',\'{val["strName"]}\')">Установить</button>'
    else:
        html += f': {v}'
    return html


def dict_to_html(d):
    html = "<ul>"
    for key, value in d.items():
        if isinstance(value, dict):
            s = htmlVal(value)
            html += f"<details><summary>{key}{s}</summary>{dict_to_html(value)}</details>"
        elif isinstance(value, list):
            html += f'<li>{key}: <select>'
            for item in value:
                html += f"<option value='{item}'>{item}</option>"
            html += "</select></li>"
        else:
            html += f"<li>{key}: {value}</li>"
    html += "</ul>"
    return html
