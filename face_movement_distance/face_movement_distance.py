import numpy as np
import cv2
import csv

def get_movement_distance(cap, frame_interval):
    cur_frame = 1.0
    last_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT) - 30
    while cur_frame <= last_frame:
        cap.set(cv2.CAP_PROP_POS_FRAMES, cur_frame)
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)  # 좌우 대칭
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.05, 5)

        if len(faces):
            for (x, y, w, h) in faces:
                p = str(x) + ', ' + str(y)
                print(p)
        k = cv2.waitKey(30) & 0xff
        if k == 27 or k == ord('q'):  # Esc 키를 누르면 종료
            break
        cur_frame += frame_interval

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
base = '../data/'
file_name='sample.avi'
cap = cv2.VideoCapture(base + file_name)
frame_interval = 100
f = open(base+file_name, 'w', encoding='utf-8-sig')
writer = csv.writer(f)

get_movement_distance(cap, frame_interval)


