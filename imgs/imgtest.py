import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
files = os.listdir('.')
x = range(2560)
imgs = []
gimgs = []
x = range(2560)


def colormap(img):
    min_val = 120  # Минимальный порог
    max_val = 130  # Максимальный порог

    # Создаем маски для значений за пределами диапазона
    mask_below = img < min_val
    mask_above = img > max_val

    # Обрезаем значения за пределами диапазона
    img_clipped = np.clip(img, min_val, max_val)

    # Нормализуем изображение в диапазоне [0, 255]
    #img_normalized = cv2.normalize(img_clipped, None, 0, 255, cv2.NORM_MINMAX)
    img_normalized = np.uint8(255 * (img_clipped - min_val) / (max_val - min_val))
    # Применяем цветовую карту JET
    colored_img = cv2.applyColorMap(img_normalized, cv2.COLORMAP_JET)

    # Применяем черный цвет к значениям ниже порога
    colored_img[mask_below] = [0, 0, 0]

    # Применяем белый цвет к значениям выше порога
    colored_img[mask_above] = [255, 255, 255]
    return colored_img






print(cv2.NORM_MINMAX)
for fname in files:
    if fname[-3: ] != 'img':
        continue
    with open(fname, 'br') as fl:
        img = fl.read()
        img = np.frombuffer(img, dtype=np.uint16).reshape(1024,2560)
        print(fname, img.mean())
        nimg = (img/(16*5)).astype(np.uint8)
        print(nimg[nimg>50].min(), nimg.max())
        # nimg[nimg==0] = 100
        gimg = cv2.applyColorMap(nimg, cv2.COLORMAP_JET)
        cv2.imshow(fname, cv2.resize(colormap(nimg),(800, 600)))
        plt.plot(x, img[300]//16)
        imgs.append(img)
        gimgs.append(gimg)
#plt.plot(x, gimgs[1][300,])
cv2.waitKey(1)
plt.show()
