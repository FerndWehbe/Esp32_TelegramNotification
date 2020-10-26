from datetime import datetime, timedelta
from configparser import ConfigParser
from urllib.request import urlopen
from bot_telegram import *
from PIL import Image
import numpy as np
import cv2


config = ConfigParser()
config.read("config-original.ini")

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

URL = config.get("espcam", "url")
MINUTES = config.get("espcam", "time")
CAMERA_BUFFER_SIZE=4096
stream = urlopen(URL)
secbytes = b''

time_last_msg = 0
count_face = 0

def notify(array_img):
    image = Image.fromarray(array_img, 'RGB')
    image.save('image.png')
    send_msg("Movimento detectado pela camera!")
    send_image(open('image.png', 'rb'))

while True:
    secbytes += stream.read(CAMERA_BUFFER_SIZE)
    jpghead = secbytes.find(b'\xff\xd8')
    jpgend = secbytes.find(b'\xff\xd9')

    if jpghead > -1 and jpgend > -1:
        jpg = secbytes[jpghead:jpgend+2]
        secbytes = secbytes[jpgend+2:]
        img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

        v = cv2.flip(img, 0)
        h = cv2.flip(img, 1)
        p = cv2.flip(img, -1)
        
        frame = p

        img = cv2.resize(frame, (800, 600))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.1,
            minNeighbors = 5,
            minSize = (30, 50)
        )

        for (x, y, width, height) in faces:
            cv2.rectangle(img, (x, y), (x+width, y+height), (0, 255, 0), 2)

        if count_face != len(faces):
            count_face = len(faces)
            if count_face > 0:
                if not time_last_msg:
                    time_last_msg = datetime.now()
                    notify(img)
                else:
                    if datetime.now() - time_last_msg > timedelta(minutes=MINUTES):
                        time_last_msg = datetime.now()
                        notify(img)
                    else:
                        count_face = 0