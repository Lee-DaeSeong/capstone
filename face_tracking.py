import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)  # 노트북 웹캠을 카메라로 사용
cap.set(3, 640)  # 너비
cap.set(4, 480)  # 높이

while (True):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # 좌우 대칭
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.05, 5)

    if len(faces):
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            p = str(x) + ', ' + str(y)
            cv2.putText(frame, p, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
    cv2.imshow('result', frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27 or k == ord('q'):  # Esc 키를 누르면 종료
        break

cap.release()
cv2.destroyAllWindows()