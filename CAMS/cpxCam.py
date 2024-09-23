import time
import threading
import logging
import ctypes
import queue
from .FrameHeaders import c_frame
from .sysHeaders import getDevices
from .mvlib import MvLib
from . import Utils
from .nodes import getNode, setNode, cmdNode, NodeError, getNodeList
from .frame import frame
from .errors import get_err


class BaseCpxCam():
    def __init__(self, dev):
        self.handle = ctypes.c_int64(0)
        self.CreateVaribles()
        self.info = Utils.get_device_info(dev)
        self.Key = self.info['chSerialNumber']
        self.Name = self.info['chUserDefinedName']
        self.minID = 0
        self.SocketMode = 0
        if self.info["Type"] == 'GigE':
            self.minID = 1
        self.connected = 0
        if self.Name == '':
            self.Name = self.Key
        self.dev = dev
        self.Start = True
        while not self.open():
            time.sleep(1)
        MvLib.MV_CC_StartGrabbing(self.handle)
        time.sleep(0.3)
        MvLib.MV_CC_StopGrabbing(self.handle)
        self.connected = 1
        self.getCamParametrs()
        logging.info('GRABBER Подключена камера:'+self.Name+str((self.Width, self.Height, self.PixelFormat)))
        self.wrTreads = []
        for i in range(1):
            Work = threading.Thread(target=self.work_thread_Win, daemon=True)
            Work.start()
            self.wrTreads.append(Work)
        self.Control = threading.Thread(target=self.controlTread, daemon=True)
        self.Control.start()

    def errProc(self, msg, ret):
        if ret == 0:
            return False
        logging.error('GRABBER '+self.Name+' '+msg+' '+get_err(ret, 1))
        return True

    def open(self):
        ret = MvLib.MV_CC_CreateHandleWithoutLog(ctypes.byref(self.handle), self.dev)
        if self.errProc('CreateHandle', ret):
            return False
        if self.info["Type"] == 'GigE':
            IP = self.info.get('nCurrentIp', '0.0.0.0')
            nIP = self.info.get('nNetExport', '0.0.0.0')
            if not Utils.validIP(IP, nIP):
                IP = Utils.getValidIp(nIP)
                ret = MvLib.MV_GIGE_ForceIpEx(self.handle, Utils.intIP(IP), 0xFFFFFF00, 0)
                if not self.errProc('ForceIp '+IP+' ', ret):
                    self.info['nCurrentIp'] = IP
                    logging.info('GRABBER '+self.Name+' '+'IP изменен на '+IP)
                    self.info['txtInfo'] += 'IP камры изменен на '+IP+'\n'
        ret = MvLib.MV_CC_OpenDevice(self.handle, ctypes.c_uint32(1), ctypes.c_uint16(0))
        if self.errProc('OpenDevice', ret):
            return False
        self.setTransMode()
        ret = MvLib.MV_CC_SetImageNodeNum(self.handle, 100)
        self.errProc('SetImageNodeNum 100', ret)
        return True

    def setTransMode(self, mode=1):
        if self.info["Type"] != 'GigE':
            self.SocketMode = 0
            return True
        ret = MvLib.MV_GIGE_SetNetTransMode(self.handle, ctypes.c_uint(mode))
        if ret == 0 and mode == 1:
            logging.info('GRABBER драйвер загружен')
            self.SocketMode = 0
            return True
        self.SocketMode = 1
        logging.warning('GRABBER работа в режиме сокета ERR: '+get_err(ret, 1))
        return False

    def close(self):
        self.stopGrabbing()
        self.Start = False
        ret = MvLib.MV_CC_CloseDevice(self.handle)
        self.errProc('CloseDevice', ret)
        MvLib.MV_CC_DestroyHandle(ctypes.byref(self.handle))

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
        self.fpsT = []
        self.frameBuffer = queue.Queue()
        self.maxBufferSize = 20
        self.TimeStampF = 1000000000
        self.frame = frame(None)
        self.scale = 0.1
        self.Width = 320
        self.Height = 200
        self.PixelFormat = 'Mono8'
        self.startTime = time.time()

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
        self.dev = None
        self.dev = getDevices(Key=self.Key)
        while self.dev is None:
            logging.error('GRABBER '+self.Name+' Камера не найдена ')
            time.sleep(1)
            self.dev = getDevices(Key=self.Key)
        logging.info('GRABBER '+self.Name+' Камера найдена')
        print(self.dev)
        print(Utils.get_device_info(self.dev)['txtInfo'])
        MvLib.MV_CC_StartGrabbing(self.handle)
        time.sleep(0.3)
        MvLib.MV_CC_StopGrabbing(self.handle)
        while not self.open():
            time.sleep(1)
        MvLib.MV_CC_StopGrabbing(self.handle)
        self.connected = 1
        self.setNodes()
        if self.isGrab:
            self.startGrabbing()

    def getNode(self, Node):
        return getNode(self.handle, Node)

    def setNode(self, Node, Value):
        if self.connected == 0:
            return
        res = setNode(self.handle, Node, Value)
        if not(res):
            info = 'GRABBER '+self.Name+' Не удалось установить '+str(Node)+' в '+str(Value)+' :'+NodeError['LastErr']
            logging.error(info)
            return
        if Node == 'Width':
            self.Width = int(Value)
        elif Node == 'Height':
            self.Height = int(Value)
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

    def getNodeList(self):
        return getNodeList(self.handle)

    def getNodeHtml(self):
        return Utils.dict_to_html(getNodeList(self.handle))

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
        self.nPayloadSize = self.getNode("PayloadSize")
        self.setNode("AcquisitionMode", "Continuous")
        self.data_buf = (ctypes.c_ubyte * self.nPayloadSize)()
        if callFunc:
            self.callFunc = callFunc
        ret = MvLib.MV_CC_StartGrabbing(self.handle)
        if self.errProc('StartGrabbing', ret):
            return False
        self.isGrab = 1
        self.startFrame = 1
        self.startTime = time.time()
        info = 'GRABBER '+self.Name+' Запущен поток '
        self.Lost = 0
        info += str((self.Width, self.Height))+' '+str(self.PixelFormat)
        logging.info(info)
        return True

    def stopGrabbing(self):
        ret = MvLib.MV_CC_StopGrabbing(self.handle)
        if self.errProc('StopGrabbing', ret):
            return False
        self.isGrab = 0
        logging.info('GRABBER '+self.Name+' Остановлен поток')
        self.FPS = 0
        return True

    def getFps(self, frame):
        if frame.TimeStamp:
            timeStamp = self.frame.TimeStamp
            dt = timeStamp - self.lastTimeStamp
            if dt:
                self.FPS = round(self.TimeStampF/dt, 3)
            self.lastTimeStamp = timeStamp
        else:
            timeStamp = self.frame.frameT
            dt = timeStamp - self.lastTimeStamp
            if dt:
                FPS = 1/dt
                self.lastTimeStamp = timeStamp
                self.fpsT.append(FPS)
            self.FPS = round(sum(self.fpsT)/len(self.fpsT), 3)
            if len(self.fpsT) > 20:
                self.fpsT.pop(0)

    def frameProc(self):
        self.frame = self.frameBuffer.get()
        self.Height = self.frame.Height
        self.Width = self.frame.Width
        if self.startFrame:
            self.frameID = self.frame.ID - 1
            self.startFrame = 0
        self.frameID += 1
        lost = self.frame.ID - Utils.getID(self.frameID, self.minID)
        self.getFps(self.frame)
        self.Lost += lost
        self.frameID += lost
        FrameDict = {}
        FrameDict['Type'] = 'Img'
        FrameDict['CamName'] = self.Name
        FrameDict['Img'] = self.frame.Img
        FrameDict['ID'] = self.frameID
        FrameDict['LastLost'] = lost
        FrameDict['FPS'] = self.FPS
        FrameDict['AllLost'] = self.Lost
        FrameDict['TimeStamp'] = self.frame.frameT
        FrameDict['Key'] = self.Key
        FrameDict['PixelType'] = self.frame.sPixelType
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
        status['Speed'] = str(round(self.FPS*self.Height*self.Width*8*10**-6, 3))+' Mbit'
        status['PixeFormat'] = self.PixelFormat
        status['PixelType'] = self.frame.sPixelType
        status['Height'] = self.Height
        status['Width'] = self.Width
        status['Lost'] = self.Lost
        status['Grabing'] = bool(self.isGrab)
        status['Connect'] = bool(self.isConnected())
        status['DriverOn'] = not bool(self.SocketMode)
        status['PreImg'] = self.frame.getPreImg(scale=self.scale)
        status['Info'] = self.info['txtInfo']
        status['BuffLen'] = self.frameBuffer.qsize()
        dt = int(time.time() - self.startTime)
        status['GrabTime'] = str(dt//3600)+':'+str((dt//60) % 60)+':'+str(dt % 60)
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

    def work_thread_Win(self):
        stOutFrame = c_frame()
        print('StartWorkThread')
        ctypes.memset(ctypes.byref(stOutFrame), 0, ctypes.sizeof(stOutFrame))
        while self.Start:
            if self.isGrab == 0:
                time.sleep(0.01)
                continue
            ret = MvLib.MV_CC_GetImageBuffer(self.handle, ctypes.byref(stOutFrame), 100)
            if ret == 0:
                self.frameBuffer.put(frame(stOutFrame))
                MvLib.MV_CC_FreeImageBuffer(self.handle, ctypes.byref(stOutFrame))
            else:
                time.sleep(0.001)
                if not self.isConnected():
                    self.resume()

    def controlTread(self):
        while self.Start:
            self.frameProc()
            if self.callFunc is not None:
                self.callFunc(self.outFrames.pop(0))
