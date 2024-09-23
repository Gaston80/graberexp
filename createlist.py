import time
import cv2
import base64
import json
from settings import image_path
import _thread
import queue

frames = queue.Queue()

def savePhoto():
    while 1:
        data = frames.get()
        img = data.get('Img')
        if img.mean() < 100:
            continue
        CamName = data.get('CamName').strip(' ')
        # ~ cv2.imwrite(image_path+'/'+str(int(time.time()*100))+'-'+CamName+'.jpg', img)
        fname = image_path+'/'+str(int(time.time()*100))+'-'+CamName+'.img'
        with open(fname, 'bw') as fl:
            fl.write(img)
        # ~ time.sleep(1)


_thread.start_new_thread(savePhoto,())
