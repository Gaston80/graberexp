import numpy as np
import matplotlib.pyplot as plt
import cv2
print(2560*1024*2, 5242880)
#l=5242880
Coord3D_C16 = 17825976
#pBufAddr : <CAMS.FrameHeaders.LP_c_ubyte object at 0x72ac9a9011c0>
stFrameInfo = {'nWidth': 2560, 'nHeight': 1024, 'enPixelType': 17825976, 'nFrameNum': 1, 'nDevTimeStampHigh': 38806, 'nDevTimeStampLow': 393230720,
                'nReserved0': 0, 'nHostTimeStamp': 1723195570199, 'nFrameLen': 5242880, 'nSecondCount': 0, 'nCycleCount': 0, }
#nRes : <CAMS.FrameHeaders.c_uint_Array_16 object at 0x72ac9a9010c0>
img = open('172527666286-RM01 -B327.img', 'br').read()
img = np.frombuffer(img, dtype=np.uint16).reshape(1024,2560)
print(img.shape)
y = img[123]
img2 = ((img%16)*16).astype(np.uint8)
x = range(2560)
print(y[1110:1120])
br = []
for i in x:
    br.append(img[0, i]%16 +16*img[1,i]%16)
plt.plot(x,y//16)
plt.plot(x,img[0]%16)
plt.plot(x,img[1]%16)
normalized_height_map = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# Применение цветовой карты (градиента)
colored_height_map = cv2.applyColorMap(normalized_height_map, cv2.COLORMAP_JET)

# Отображение изображения с использованием Matplotlib
cv2.imshow('1',cv2.resize(colored_height_map,(800,600)))
cv2.waitKey(1)
#plt.plot(x,img[3]%16)
#plt.plot(x,img[2])

plt.show()
