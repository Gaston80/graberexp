from CAMS import getGigEDevices, genicam, getInfo
from flask import Flask, Response, render_template, request, send_from_directory
import time
import json
import cv2
import os
import numpy as np
from datetime import datetime
from createlist import frames
from settings import Nodes, camSettings, image_path, Cams


def onImg(data):
    frames.put(data)
    if frames.qsize() > 100:
        frames.get()


def startCam(dev):
    cam = genicam(dev)
    lNodes = Nodes+camSettings.get(cam.Key, {}).get('Nodes', [])
    cam.setNodes(lNodes)
    Cams.append(cam)
    cam.startGrabbing(callFunc=onImg)


CamList = []
devs = getGigEDevices()
while len(devs) == 0:
    print('No cams in system trying again')
    time.sleep(1)
    devs = getGigEDevices()


for dev in devs:
    info = getInfo(dev)
    print(info['txtInfo'])
    print('-----------------')
N = 0


devlist = ['RM01 -B325', 'RM01 -B325']
for dev in devs:
    info = getInfo(dev)
    #if info['chUserDefinedName'] in devlist:
    startCam(dev)

Cam = Cams[0]
startTime = time.time()
app = Flask(__name__)


def generate_frames(N, W=0):
    while True:
        frame = Cams[N].getLastImg()
        flip = camSettings.get(Cams[N].Key, {}).get('Flip', 0)
        if Cams[N].frame.sPixelType == 'Coord3DC16':
            frame = (frame/(16*5)).astype(np.uint8)
            frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)

        if flip:
            frame = cv2.flip(frame, 0)
        if W:
            H0, W0 = frame.shape[0:2]
            H = int(H0*W/W0)
            if H < 100:
                H = 100
            frame = cv2.resize(frame, (W, H))
        ret, img = cv2.imencode('.jpg', frame)
        frame = img.tobytes()
        out = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
        out += frame + b'\r\n'
        yield out
        time.sleep(0.1)


def generate_txt(N):
    while 1:
        camlist = []
        out = {'Камеры': '-----------------'}
        data = Cams[N].getStatus()
        data.pop('PreImg')
        data['Pos'] = ''
        for k in data.keys():
            out[k] = []
        for cam in Cams:
            camlist.append(cam.Name)
            info = cam.getStatus()
            info.pop('PreImg')
            info['Pos'] = camSettings.get(cam.Key, {}).get('OutName', cam.Name)
            for k, v in info.items():
                out[k].append(v)

        out['CamsCount'] = len(Cams)
        out['Очередь'] = frames.qsize()
        dt = int(time.time() - startTime)
        out['Время работы'] = str(dt//3600)+':'+str((dt//60) % 60)+':'+str(dt % 60)
        out['camlist'] = camlist
        # out['Контроллер'] = '-----------------'
        # out.update(controllerDict)
        important = {}
        important['Важное'] = '-----------------'
        important['Камера'] = out.get('Pos')
        important['FPS'] = out.get('FPS')
        important['Потери Кадров'] = out.get('Lost')
        important['Работа'] = out.get('Grabing')
        out['important'] = important
        txt = json.dumps(out)
        yield "data:"+txt+"\n\n"  # Событие 1 с разделителем
        time.sleep(0.1)


@app.route('/img')
def getImg():
    N = request.args.get('N', 0)
    N = int(N)
    print('getimg', N)
    img = Cams[N].getLastImg()
    ret, img = cv2.imencode('.jpg', img)
    frame = img.tobytes()
    out = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
    out += frame + b'\r\n'
    return Response(frame, mimetype='image/jpeg')


@app.route('/cmd')
def cmd():
    cmd = request.args.get('cmd')
    N = request.args.get('N', 0)
    allcams = request.args.get('all')
    if cmd.split()[0] == 'Exit':
        os._exit(1)
    elif cmd == 'GetImg':
        ret = "<a href='/img?N="+str(N)+"'>Возьми сдесь</a>"
    else:
        if allcams == 'true':
            ret = ''
            for cam in Cams:
                ret += cam.Name+' '+cam.command(cmd)+'<br>'
        else:
            ret = Cams[int(N)].command(cmd)
    ret = json.dumps({'resp': ret})
    return(ret)


@app.route('/nodelist')
def nodelist():
    N = int(request.args.get('N', 0))
    cam = Cams[N].Name
    html = Cams[N].getNodeHtml()
    return render_template('nodelist.html', cam=cam, html=html, N=0)


@app.route('/text_stream')
def text_stream():
    N = request.args.get('N', 0)
    N = int(N)
    return Response(generate_txt(N), content_type='text/event-stream')


@app.route('/video_feed')
def video_feed():
    N = request.args.get('N', 0)
    W = request.args.get('W', 0)
    N = int(N)
    W = int(W)
    return Response(generate_frames(N, W), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return Response(open('templates/index.html', 'br').read(), content_type='text/html')


@app.route('/script.js')
def script():
    return Response(open('templates/script.js', 'br').read(), content_type='text/js')


@app.route('/styles.css')
def style():
    return Response(open('templates/stiles.css', 'br').read(), content_type='text/css')


@app.template_filter('format_time')
def format_time(seconds, format='%Y.%m.%d-%H:%M:%S'):
    try:
        txt = time.strftime(format, time.localtime(float(seconds)))
    except Exception as err:
        txt = str(err)
    return txt


# Определение маршрута для обслуживания изображений
@app.route('/static/images/<path:filename>')
def custom_static(filename):
    return send_from_directory(image_path, filename)


@app.route('/photos')
def gallery():
    image_folder = image_path
    images = []
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
            filepath = os.path.join(image_folder, filename)
            creation_time = datetime.fromtimestamp(os.path.getctime(filepath))
            images.append({'filename': filename, 'creation_time': creation_time})
    images.sort(key=lambda x: x['creation_time'], reverse=True)
    return render_template('gallery.html', images=images[:30])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
