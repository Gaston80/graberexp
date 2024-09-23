from random import randint
import time
import threading
import logging
import ctypes
from .FrameHeaders import c_frame, c_frameInfo
from .mvlib import MvLib
from . import Utils
from .nodes import getNode, setNode, cmdNode
from .frame import frame, frame2
from .sysHeaders import getGigEDevices
# from .errors import get_err

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO, datefmt='%Y.%m.%d %H:%M:%S')


def forceIP(dev, IP='', NM='255.255.255.0', GW='0.0.0.0'):
    info = Utils.getInfo(dev)
    Key = info['Key']
    if IP == '':
        IP = Utils.intIP(info['nNetExport'])
        IP -= IP % 0x10000
        IP += randint(50, 250)
        IP = Utils.strIP(IP)
        if IP == info['nNetExport']:
            IP = Utils.strIP(Utils.intIP(IP)+3)
    handle = ctypes.c_int64(0)
    if MvLib.MV_CC_CreateHandleWithoutLog(ctypes.byref(handle), dev) != 0:
        print('error handle')
        return
    ret = MvLib.MV_GIGE_ForceIpEx(
        handle,
        ctypes.c_uint(Utils.intIP(IP)),
        ctypes.c_uint(Utils.intIP(NM)),
        ctypes.c_uint(Utils.intIP(GW)))
    if ret != 0:
        print('error IP')
        return
    MvLib.MV_CC_DestroyHandle(handle)
    dev = getGigEDevices(Key)
    return dev


class BaseCam():
    def __init__(self, dev):
        self.handle = ctypes.c_int64(0)
        self.CreateVaribles()
        self.info = Utils.getInfo(dev)
        self.Key = self.info['Key']
        self.Name = self.info['chUserDefinedName']
        self.connected = 0
        if self.Name == '':
            self.Name = self.Key
        if not(Utils.validIP(self.info['nCurrentIp'], self.info['nNetExport'])):
            logging.error('GRABBER '+self.Name+' не корректный IP:'+self.info['nCurrentIp'])
            dev = forceIP(dev)
            self.info = Utils.getInfo(dev)
            logging.info('GRABBER '+self.Name+' IP изменен на '+self.info['nCurrentIp'])
        self.dev = dev
        if MvLib.MV_CC_CreateHandleWithoutLog(ctypes.byref(self.handle), dev) != 0:
            logging.error('GRABBER '+self.Name+' Error Handle')
            return
        if MvLib.MV_CC_OpenDevice(self.handle, ctypes.c_uint32(1), ctypes.c_uint16(0)) != 0:
            logging.error('GRABBER '+self.Name+' Error Open')
            return
        self.connected = 1
        self.setTransMode(1)
        self.setPaketSize()
        self.getCamParametrs()
        logging.info('GRABBER Подключена камера:'+self.Name+str((self.Width, self.Height, self.PixelFormat)))
        self.Work = threading.Thread(target=self.work_thread_Win, daemon=True)
        self.Work.start()
        self.Control = threading.Thread(target=self.controlTread, daemon=True)
        self.Control.start()

    def CreateVaribles(self):
        self.lastTimeStamp = 0
        self.FPS = 0
        self.frameID = 0
        self.Lost = 0
        self.StartFrame = 0
        self.isGrab = 0
        self.callFunc = None
        self.outFrames = []
        self.NodeList = []
        self.frameBuffer = []
        self.maxBufferSize = 20
        self.TimeStampF = 1000000000
        self.SocketMode = 1
        self.frame = frame(None)
        self.scale = 0.1
        self.Width = 320
        self.Height = 200
        self.PixelFormat = 'Mono8'

    def getCamParametrs(self):
        self.Width = self.getNode('Width')
        self.Height = self.getNode('Height')
        self.PixelFormat = self.getNode('PixelFormat')
        TimeStampF = self.getNode('GevTimestampTickFrequency')
        if TimeStampF is not None:
            self.TimeStampF = TimeStampF

    def resume(self):
        self.lastTimeStamp = 0
        self.FPS = 0
        self.frameID = 0
        self.Lost = 0
        self.StartFrame = 0
        self.connected = 0
        logging.error('GRABBER '+self.Name+' Отвалилась')
        MvLib.MV_CC_DestroyHandle(self.handle)
        self.dev = None
        while self.dev is None:
            self.dev = getGigEDevices(self.Key)
            logging.error('GRABBER '+self.Key+' не найдена')
            time.sleep(1)
        self.info = Utils.getInfo(self.dev)
        if not(Utils.validIP(self.info['nCurrentIp'], self.info['nNetExport'])):
            logging.error('GRABBER '+self.Key+' не корректный IP:'+self.info['nCurrentIp'])
            self.dev = forceIP(self.dev)
            self.info = Utils.getInfo(self.dev)
            logging.info('GRABBER '+self.Key+'IP изменен на '+self.info['nCurrentIp'])
        while MvLib.MV_CC_CreateHandleWithoutLog(ctypes.byref(self.handle), self.dev) != 0:
            logging.error('GRABBER '+self.Name+' Error Handle')
            time.sleep(0.5)
        while MvLib.MV_CC_OpenDevice(self.handle, ctypes.c_uint32(1), ctypes.c_uint16(0)) != 0:
            logging.error('GRABBER '+self.Name+' Error Open')
            time.sleep(0.5)
        self.connected = 1
        self.setTransMode()
        self.setPaketSize()
        self.setNodes()
        if self.isGrab:
            self.startGrabbing()

    def setTransMode(self, mode=1):
        ret = MvLib.MV_GIGE_SetNetTransMode(self.handle, ctypes.c_uint(mode))
        if ret == 0 and mode == 1:
            logging.info('GRABBER драйвер загружен')
            self.SocketMode = 0
            return True
        ret = ctypes.c_uint(ret)
        logging.warning('GRABBER работа в режиме сокета ERR: '+str(hex(ret.value)))
        return False

    def setPaketSize(self):
        nPacketSize = MvLib.MV_CC_GetOptimalPacketSize(self.handle)
        ret = self.setNode("GevSCPSPacketSize", nPacketSize)
        if ret:
            logging.info('GRABBER '+self.Name+' NetPacketSize: '+str(nPacketSize))

    def getNode(self, Node):
        return getNode(self.handle, Node)

    def setNode(self, Node, Value):
        if self.connected == 0:
            return
        res = setNode(self.handle, Node, Value)
        if not(res):
            logging.error('GRABBER '+self.Name+' Не удалось установить '+str(Node)+' в '+str(Value))
            return
        if Node == 'Width':
            self.Width = Value
        elif Node == 'Height':
            self.Height = Value
        elif Node == 'DeviceUserID':
            self.Name = Value
        elif Node == 'PixelFormat':
            self.PixelFormat = Value
        logging.info('GRABBER '+self.Name+' установлено '+str(Node)+' в '+str(Value))
        return res

    def setNodes(self, Nodes=[]):
        if self.connected == 0:
            return
        if len(Nodes) == 0:
            Nodes = self.NodeList
        for node in Nodes:
            ret = self.setNode(node[0], node[1])
            if ret:
                if node not in self.NodeList:
                    self.NodeList.append(node)

    def cmdNode(self, Node):
        return cmdNode(self.handle, Node)

    def setMax(self):
        w = self.getNode('WidthMax')
        self.setNode('OffsetX', 0)
        self.setNode('Width', w)
        h = self.getNode('HeightMax')
        self.setNode('OffsetY', 0)
        self.setNode('Height', h)

    def isConnected(self):
        return bool(MvLib.MV_CC_IsDeviceConnected(self.handle))

    def startGrabbing(self, callFunc=None):
        if self.connected == 0:
            return
        MvLib.MV_CC_StartGrabbing.argtype = ctypes.c_void_p
        MvLib.MV_CC_StartGrabbing.restype = ctypes.c_uint
        self.nPayloadSize = self.getNode("PayloadSize")
        self.setNode("AcquisitionMode", "Continuous")
        self.data_buf = (ctypes.c_ubyte * self.nPayloadSize)()
        if callFunc:
            self.callFunc = callFunc
        MvLib.MV_CC_StopGrabbing(self.handle)
        ret = MvLib.MV_CC_StartGrabbing(self.handle)
        if ret == 0:
            self.isGrab = 1
            self.startFrame = 1
            info = 'GRABBER '+self.Name+' Запущен поток '
            info += str((self.Width, self.Height))+' '+str(self.PixelFormat)
            logging.info(info)
            return True
        logging.error('GRABBER '+self.Name+' Не удалось запустить поток')

    def stopGrabbing(self):
        MvLib.MV_CC_StopGrabbing.argtype = ctypes.c_void_p
        MvLib.MV_CC_StopGrabbing.restype = ctypes.c_uint
        ret = MvLib.MV_CC_StopGrabbing(self.handle)
        if ret == 0:
            self.isGrab = 0
            logging.info('GRABBER '+self.Name+' Остановлен поток')
            self.FPS = 0
            return True

    def frameProc(self):
        self.frame = self.frameBuffer.pop(0)
        if self.startFrame:
            self.frameID = self.frame.ID - 1
            self.startFrame = 0
        self.frameID += 1
        timeStamp = self.frame.TimeStamp
        dt = timeStamp - self.lastTimeStamp
        if dt:
            self.FPS = round(self.TimeStampF/dt, 3)
        self.lastTimeStamp = timeStamp
        lost = self.frame.ID - Utils.getID(self.frameID)
        self.Lost += lost
        self.frameID += lost
        if lost:
            info = 'GRABBER '+self.Name+' Lost frames '+str(lost)+' frame№:'
            info += str(self.frameID-lost)+' frameID:'+str(self.frame.ID)
            logging.warning(info)
        FrameDict = {}
        FrameDict['Type'] = 'Img'
        FrameDict['CamName'] = self.Name
        FrameDict['Img'] = self.frame.Img
        FrameDict['ID'] = self.frameID
        FrameDict['LastLost'] = lost
        FrameDict['FPS'] = self.FPS
        FrameDict['AllLost'] = self.Lost
        FrameDict['TimeStamp'] = self.frame.frameT
        FrameDict['dt'] = 1000 * dt // self.TimeStampF  # ms
        FrameDict['Key'] = self.Key

        self.outFrames.append(FrameDict)
        if len(self.outFrames) > self.maxBufferSize:
            self.outFrames.pop(0)

    def getStatus(self):
        status = {}
        status['Type'] = 'Status'
        status['Key'] = self.Key
        status['CamName'] = self.Name
        status['frameID'] = self.frameID
        status['FPS'] = self.FPS
        # status['Speed'] = self.FPS*self.Height*self.Width
        status['PixeFormat'] = self.PixelFormat
        status['Height'] = self.Height
        status['Width'] = self.Width
        status['Lost'] = self.Lost
        status['Grabing'] = bool(self.isGrab)
        status['Connect'] = bool(self.isConnected())
        status['SocketMode'] = bool(self.SocketMode)
        status['PreImg'] = self.frame.getPreImg(scale=self.scale)
        status['Info'] = self.info['txtInfo']
        return status

    def command(self, cmds):
        cmd = str(cmds).split()
        ret = False
        val = None
        if cmd[0] == 'Start':
            ret = self.startGrabbing()
        elif cmd[0] == 'Stop':
            ret = self.stopGrabbing()
        elif cmd[0] == 'GetImg':
            img = self.frame.getBmp()
            if img is not None:
                return img
        elif cmd[0] == 'Get' and len(cmd) > 1:
            val = self.getNode(cmd[1])
            if val is not None:
                return str(val)
        elif cmd[0] == 'Set' and len(cmd) > 2:
            ret = self.setNode(cmd[1], cmd[2])
        elif cmd[0] == 'Exec' and len(cmd) > 1:
            ret = self.cmdNode(cmd[1])
        if ret:
            return 'Done'
        return 'Error'

    def getFrame(self):
        if len(self.outFrames):
            return self.outFrames.pop(0)

    def getLastImg(self):
        return self.frame.Img

    def showLastImg(self, resize=0, width=800, name='', sensor=None):
        if name == '':
            name = self.Name
        key = self.frame.show(resize=resize, width=width, name=name, sensor=sensor)
        return key

    def setCallFunc(self, callFunc):
        self.callFunc = callFunc

    def work_thread_Linux(self):
        stFrameInfo = c_frameInfo()
        while True:
            if self.isGrab == 0:
                continue
            ret = MvLib.MV_CC_GetOneFrameTimeout(
                self.handle,
                ctypes.byref(self.data_buf),
                self.nPayloadSize,
                ctypes.byref(stFrameInfo), 1000)
            if ret == 0:
                self.frameBuffer.append(frame2(self.data_buf, self.nPayloadSize, stFrameInfo))
            else:
                ret = ctypes.c_uint(ret)
                # print('getframeErr', hex(ret.value))
                time.sleep(0.01)
                self.FPS = 0

    def work_thread_Win(self):
        stOutFrame = c_frame()
        while True:
            if self.isGrab == 0:
                time.sleep(0.1)
                continue
            ret = MvLib.MV_CC_GetImageBuffer(self.handle, ctypes.byref(stOutFrame), 1000)
            if ret == 0:
                self.frameBuffer.append(frame(stOutFrame))
                MvLib.MV_CC_FreeImageBuffer(self.handle, ctypes.byref(stOutFrame))
            else:
                ret = ctypes.c_uint(ret)
                time.sleep(0.01)
                self.FPS = 0
                # print('getframeErr', hex(ret.value))

    def controlTread(self):
        while 1:
            while len(self.frameBuffer):
                self.frameProc()
                if self.callFunc is not None:
                    self.callFunc(self.outFrames.pop(0))
            if not self.isConnected():
                self.resume()
            time.sleep(0.01)
