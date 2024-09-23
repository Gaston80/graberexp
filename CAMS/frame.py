import numpy as np
import cv2
import time
# from . import Utils
from . import pixels


class frame():
    def __init__(self, c_frame):
        if c_frame is None:
            self.createBlanc()
            return
        self.ID = c_frame.stFrameInfo.nFrameNum
        self.Width = c_frame.stFrameInfo.nWidth
        self.Height = c_frame.stFrameInfo.nHeight
        self.PixelType = c_frame.stFrameInfo.enPixelType
        self.sPixelType = pixels.get_pixel_type(self.PixelType)
        self.TimeStamp = (c_frame.stFrameInfo.nDevTimeStampHigh << 32) | c_frame.stFrameInfo.nDevTimeStampLow
        self.FrameLen = c_frame.stFrameInfo.nFrameLen
        self.frameT = time.time()
        self.Input = c_frame.stFrameInfo.nInput
        self.Gain = c_frame.stFrameInfo.fGain
        self.ExposureTime = c_frame.stFrameInfo.fExposureTime
        self.AverageBrightness = c_frame.stFrameInfo.nAverageBrightness
        self.Output = c_frame.stFrameInfo.nOutput
        pBuff = c_frame.pBufAddr
        self.Img = np.ctypeslib.as_array(pBuff, (self.Height, self.Width)).astype(np.uint8)

        if self.PixelType == 17301513:  # BayerRG8
            self.Img = cv2.cvtColor(self.Img, 46)
        if self.PixelType == 17825976:
            img = np.ctypeslib.as_array(pBuff, (self.FrameLen, )).astype(np.uint8).tobytes()
            self.Img = np.frombuffer(img, dtype=np.uint16).reshape(self.Height, self.Width)
            # open('static/img.img', 'bw').write(img.tobytes())

    def createBlanc(self):
        self.ID = 0
        self.Width = 320
        self.Height = 200
        self.PixelType = 0
        self.sPixelType = pixels.get_pixel_type(self.PixelType)
        self.TimeStamp = 0
        self.Inputs = 0
        self.FrameLen = 0
        self.Gain = 0
        self.ExposureTime = 0
        self.AverageBrightness = 0
        self.Output = 0
        self.frameT = time.time()
        self.Img = np.zeros((200, 320), dtype=np.uint8)

    def show(self, resize=0, width=800, name='', sensor=None):
        img = self.Img
        w = width
        if not name:
            name = 'img'
        if resize:
            h = int(w*self.Height/self.Width)
            img = cv2.resize(img, (w, h))
        if sensor is not None:
            x1 = w // 2 + 10
            x2 = x1 - 20
            if h > 20:
                y1 = 10
                y2 = 20
            else:
                y1 = 0
                y2 = h
            if sensor:
                color = (0, 255, 0)
            else:
                color = (0, 0, 255)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)
        cv2.imshow(name, img)
        key = cv2.waitKey(1)
        return key

    def getPreImg(self, scale=0.1, imtype='.jpg'):
        w = int(self.Width*scale)
        h = int(self.Height*scale)
        if h * w == 0:
            return
        img = cv2.resize(self.Img, (w, h))
        ok, img = cv2.imencode(imtype, img)
        if not ok:
            return
        return img.tobytes()

    def getBmp(self):
        ret, img = cv2.imencode('.bmp', self.Img)
        if ret:
            return img.tobytes()


class frame2(frame):
    def __init__(self, data, size, c_frame, blanc=False):
        if c_frame is None:
            self.createBlanc()
            return
        self.ID = c_frame.nFrameNum
        self.Width = c_frame.nWidth
        self.Height = c_frame.nHeight
        self.PixelType = c_frame.enPixelType
        self.TimeStamp = self.TimeStamp = (c_frame.nDevTimeStampHigh << 32) | c_frame.nDevTimeStampLow
        self.FrameLen = c_frame.nFrameLen
        self.Inputs = c_frame.nInput
        self.frameT = time.time()
        self.Img = np.frombuffer(data, dtype=np.uint8).reshape(self.Height, self.Width)

    def getImg(self):
        self.Img = np.ctypeslib.as_array(self.pBuff).astype(np.uint8).reshape(self.Height, self.Width)
        if self.PixelType == 17301513:  # BayerRG8
            self.Img = cv2.cvtColor(self.Img, 46)
