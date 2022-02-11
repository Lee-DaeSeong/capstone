import numpy as np
import cv2

# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontface.xml')
cap = cv2.VideoCapture(0)  # 노트북 웹캠을 카메라로 사용
cap.set(3, 640)  # 너비
cap.set(4, 480)  # 높이

prev_x, prev_y = 0, 0
detect = False
move=0
prev=0
frame_cnt=0
res=0
while (True):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # 좌우 대칭
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.05, 5)
    cur_x, cur_y = 0, 0
    if len(faces):
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            p = str(x) + ', ' + str(y)
            cv2.putText(frame, p, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
            cur_x, cur_y = x, y

            move += abs(prev_x-cur_x) + abs(prev_y-cur_y)
            if frame_cnt == 50:
                print(move, prev)
                if move > (prev * 1.45):
                    print(0)
                elif move > (prev * 1.32):
                    print(1)
                else:
                    print(2)
                prev = move
                frame_cnt=0
                move=0
                res=0
            frame_cnt+=1
            detect=True
    else:
        prev_x, prev_y = 0, 0
        detect = False
    if detect:
        prev_x, prev_y = cur_x, cur_y

    cv2.imshow('result', frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27 or k == ord('q'):  # Esc 키를 누르면 종료
        break

cap.release()
cv2.destroyAllWindows()