import ctypes
from . import nodesHeaders as nd
from .mvlib import MvLib
from .errors import get_err
from . import Utils
NodeError = {'lastErr': 'None'}


def SetIntValue(handle, strKey, nValue):
    try:
        nValue = int(nValue)
    except Exception as err:
        NodeError['x'] = str(err)
        return 0x80190009
    return MvLib.MV_CC_SetIntValue(handle, strKey.encode('ascii'), ctypes.c_uint32(nValue))


def SetEnumValueByString(handle, strKey, sValue):
    sValue = str(sValue)
    return MvLib.MV_CC_SetEnumValueByString(handle, strKey.encode('ascii'), sValue.encode('ascii'))


def SetFloatValue(handle, strKey, fValue):
    try:
        fValue = float(fValue)
    except Exception as err:
        NodeError['x'] = str(err)
        return 0x80190009
    return MvLib.MV_CC_SetFloatValue(handle, strKey.encode('ascii'), ctypes.c_float(fValue))


def SetBoolValue(handle, strKey, bValue):
    try:
        bValue = bool(bValue)
    except Exception as err:
        NodeError['x'] = str(err)
        return 0x80190009
    return MvLib.MV_CC_SetBoolValue(handle, strKey.encode('ascii'), bValue)


def SetStringValue(handle, strKey, sValue):
    sValue = str(sValue)
    return MvLib.MV_CC_SetStringValue(handle, strKey.encode('ascii'), sValue.encode('ascii'))


def cmdNode(handle, strKey):
    ret = MvLib.MV_CC_SetCommandValue(handle, strKey.encode('ascii'))
    if ret == 0:
        return True
    else:
        NodeError['LastErr'] = get_err(ret, 1)
        return False


def GetEnumValue(handle, strKey):
    val = nd.MVCC_ENUMVALUE_T()
    ret = MvLib.MV_CC_GetEnumValue(handle, strKey.encode('ascii'), ctypes.byref(val))
    if ret == 0:
        return val.nCurValue
    else:
        NodeError['LastErr'] = get_err(ret, 1)


def GetEnumTxtValue(handle, strKey):
    val = nd.MVCC_ENUMENTRY()
    num = GetEnumValue(handle, strKey)
    if num is None:
        return
    val.nCurValue = num
    ret = MvLib.MV_CC_GetEnumEntrySymbolic(handle, strKey.encode('ascii'), ctypes.byref(val))
    if ret == 0:
        return val.chSymbolic.decode()
    else:
        NodeError['LastErr'] = get_err(ret, 1)
        return num


def getEmumTxt(handle, key, num):
    val = nd.MVCC_ENUMENTRY()
    val.nCurValue = num
    MvLib.MV_CC_GetEnumEntrySymbolic(handle, key.encode('ascii'), ctypes.byref(val))
    return val.chSymbolic.decode()


def GetFloatValue(handle, strKey):
    val = ctypes.c_float(0)
    ret = MvLib.MV_CC_GetFloatValue(handle, strKey.encode('ascii'), ctypes.byref(val))
    if ret == 0:
        return val.value
    else:
        NodeError['LastErr'] = get_err(ret, 1)


def GetBoolValue(handle, strKey):
    val = ctypes.c_bool(0)
    ret = MvLib.MV_CC_GetBoolValue(handle, strKey.encode('ascii'), ctypes.byref(val))
    if ret == 0:
        return val.value


def GetIntValue(handle, strKey):
    val = ctypes.c_uint(0)
    ret = MvLib.MV_CC_GetIntValue(handle, strKey.encode(), ctypes.byref(val))
    if ret == 0:
        return val.value
    else:
        NodeError['LastErr'] = get_err(ret, 1)


def GetStrValue(handle, strKey):
    val = nd.MVCC_STRINGVALUE_T()
    ret = MvLib.MV_CC_GetStringValue(handle, strKey.encode(), ctypes.byref(val))
    if ret == 0:
        return val.chCurValue.decode()
    else:
        NodeError['LastErr'] = get_err(ret, 1)


def getNodeType(handle, Node):
    val = ctypes.c_int(0)
    types = ['Value', 'Base', 'Int', 'Bool', 'Cmd', 'Float', 'Str', 'Reg', 'Cat', 'Enum', 'EnumE', 'Port']
    ret = MvLib.MV_XML_GetNodeInterfaceType(handle, Node.encode(), ctypes.byref(val))
    if ret:
        NodeError['LastErr'] = get_err(ret, 1)
        # print(get_err(ret, 1))
        return 'Err'
    return types[val.value]


def getNode(handle, Node):
    t = getNodeType(handle, Node)
    if t == 'Int':
        return GetIntValue(handle, Node)
    elif t == 'Bool':
        return GetBoolValue(handle, Node)
    elif t == 'Float':
        return GetFloatValue(handle, Node)
    elif t == 'Str':
        return GetStrValue(handle, Node)
    elif t == 'Enum':
        return GetEnumTxtValue(handle, Node)


def setNode(handle, Node, val):
    t = getNodeType(handle, Node)
    if t == 'Int':
        ret = SetIntValue(handle, Node, val)
    elif t == 'Bool':
        ret = SetBoolValue(handle, Node, val)
    elif t == 'Float':
        ret = SetFloatValue(handle, Node, val)
    elif t == 'Str':
        ret = SetStringValue(handle, Node, val)
    elif t == 'Enum':
        ret = SetEnumValueByString(handle, Node, val)
    elif t == 'Cmd':
        ret = cmdNode(handle, Node)
    elif t == 'Err':
        ret = 0x80190009
    if ret == 0:
        return True
    else:
        NodeError['LastErr'] = get_err(ret, 1)
        return False


def setNodes(handle, Nodes):
    for node in Nodes:
        key, val = node[:2]
        if setNode(handle, key, val):
            print('+ Ok Установлено', key, 'в', val)
        else:
            print('- ERR Не удалось установить', key, 'в', NodeError['LastErr'])


def getChild(handle, catNode):
    NodeList = {}
    cNodeList = nd.MV_XML_NODES_LIST()
    MvLib.MV_XML_GetChildren(handle, ctypes.byref(catNode), ctypes.byref(cNodeList))
    for i in range(cNodeList.nNodeNum):
        node = Utils.structure_to_dict(cNodeList.stNodes[i])
        node["enType"] = nd.NodeTypes[node["enType"]]
        if node["enType"] == 'Cat':
            NodeList[node['strDisplayName']] = getChild(handle, cNodeList.stNodes[i])
        elif node["enType"] == 'Enum':
            NodeList[node['strDisplayName']] = node
            val = nd.MVCC_ENUMVALUE_T()
            MvLib.MV_CC_GetEnumValue(handle, node['strName'].encode('ascii'), ctypes.byref(val))
            vals = []
            for j in range(val.nSupportedNum):
                vals.append(getEmumTxt(handle, node['strName'], val.nSupportValue[j]))
            node['nSupportValue'] = vals
            node['CurrentValue'] = GetEnumTxtValue(handle, node['strName'])
        elif node["enType"] == 'Bool':
            NodeList[node['strDisplayName']] = node
            node['CurrentValue'] = GetBoolValue(handle, node['strName'])
        elif node["enType"] == 'Float':
            NodeList[node['strDisplayName']] = node
            node['CurrentValue'] = GetFloatValue(handle, node['strName'])
        elif node["enType"] == 'Int':
            NodeList[node['strDisplayName']] = node
            node['CurrentValue'] = GetIntValue(handle, node['strName'])
        elif node["enType"] == 'Str':
            NodeList[node['strDisplayName']] = node
            node['CurrentValue'] = GetStrValue(handle, node['strName'])
        elif node["enType"] == 'Cmd':
            NodeList[node['strDisplayName']] = node
            node['CurrentValue'] = 'Exec'
        else:
            NodeList[node['strDisplayName']] = node
        node.pop('strDisplayName')
        node.pop('strDescription')
    return NodeList


def getNodeList(handle):
    NodeList = {}
    nodes = nd.MV_XML_NODE_FEATURE()
    ret = MvLib.MV_XML_GetRootNode(handle, ctypes.byref(nodes))
    nodelist = nd.MV_XML_NODES_LIST()
    ret = MvLib.MV_XML_GetChildren(handle, ctypes.byref(nodes), ctypes.byref(nodelist))
    for i in range(nodelist.nNodeNum):
        node = Utils.structure_to_dict(nodelist.stNodes[i])
        NodeList[node['strDisplayName']] = getChild(handle, nodelist.stNodes[i])
    return NodeList
