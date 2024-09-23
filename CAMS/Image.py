import numpy as np


class ImageClass:
    def __init__(self, Width, Height, PixHeght=0, Color=0, MinHeight=1024):
        self.Width = Width
        self.Height = Height
        self.Color = Color
        self.Counter = 0
        if Color == 0:
            self.OutImg = np.zeros((Height, Width), np.uint8)
            self.LastImg = self.OutImg.copy()
        else:
            self.OutImg = np.zeros((Height, Width, 3), np.uint8)
            self.LastImg = self.OutImg.copy()
        self.MinHeight = MinHeight
        self.Pos = 0
        self.PixHeght = PixHeght
        self.OutBuff = []

    def add(self, img, Lost=0):
        H, W = img.shape[0:2]
        Ret = 0
        if Lost:
            Black = img.copy()
            Black[True] = 0
            for i in range(Lost):
                Ret += self.ImgProc(Black)
        Ret += self.ImgProc(img)
        return Ret

    def ImgProc(self, img):
        Ret = 0
        H, W = img.shape[0:2]
        if (H+self.Pos) <= self.Height:
            self.OutImg[self.Pos:self.Pos+H] = img
            self.Pos += H
        else:
            rsd = H+self.Pos-self.Height
            self.OutImg[self.Pos:] = img[:H-rsd]
            Ret = 1
            self.OutBuff.append((self.OutImg))
            self.OutImgReset()
            self.OutImg[:H-rsd] = img[rsd:]
            self.Pos = H-rsd

        if self.Pos == self.Height:
            Ret = 1
            self.Pos = 0
            self.OutBuff.append((self.OutImg.copy()))
            self.OutImgReset()
        return Ret

    def OutImgReset(self):
        self.LastImg = self.OutImg.copy()
        self.OutImg[True] = 0

    def getImg(self):
        if len(self.OutBuff):
            img = self.OutBuff.pop(0)
            return img
        else:
            return

    def reset(self):
        self.Pos = 0
        self.OutImgReset()
        self.LastImg = self.OutImg.copy()
        self.Counter += 1

    def getCurrentImg(self):
        H = (int(self.Pos/self.MinHeight)+1)*self.MinHeight
        OutImg = self.OutImg[:H].copy()
        self.reset()
        return OutImg
