import collections
import cv2
from gaze_tracking.gaze_tracking import GazeTracking

face_cascade = cv2.CascadeClassifier('./face_movement/haarcascade_frontface.xml')

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
gaze = GazeTracking()
prev_x, prev_y, cur_x, cur_y = 0, 0, 0, 0

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.05, 5)
    if len(faces):
        prev_x, prev_y = faces[0][0], faces[0][1]

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.05, 5)
    if len(faces):
        cur_x, cur_y = faces[0][0], faces[0][1]

    if prev_x and cur_x:
        break

move = 0
prev = abs(prev_x - cur_x) + abs(prev_y - cur_y)
move_frame_cnt = 0
move_q = collections.deque()
move_window_size = 4
max_frame_size = 5
min_movement = 10000
gaze_frame_cnt = 0
gaze_center = 0

def calc_move_point():
    global move
    global prev
    global move_frame_cnt
    global min_movement
    move_q.append(move)

    if len(move_q) == move_window_size:
        move = move_q[0] * 0.1
        move += move_q[1] * 0.1
        move += move_q[2] * 0.3
        move += move_q[3] * 0.5
        move_q.popleft()

    if move > (prev * 1.43) or move > min_movement * 5:
        print('move :', 0)
    elif move > (prev * 1.22):
        print('move :', 1)
    else:
        print('move :', 2)

    min_movement = min(min_movement, move)
    prev = move
    move_frame_cnt = 0
    move = 0

def calc_gaze_point():
    global gaze_frame_cnt
    global gaze_center

    calc_gaze = gaze_center / gaze_frame_cnt

    gaze_frame_cnt = 0
    gaze_center = 0

    # 0.828, 0.719, 0.582

    if calc_gaze > 0.828:
        print('gaze :', 2)
    elif calc_gaze > 0.719:
        print('gaze :', 1)
    else:  # 0.582
        print('gaze :', 0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.05, 5)
    cur_x, cur_y = 0, 0
    if len(faces):
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            p = str(x) + ', ' + str(y)
            cv2.putText(frame, p, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
            cur_x, cur_y = x, y

            move += abs(prev_x - cur_x) + abs(prev_y - cur_y)
            if move_frame_cnt == max_frame_size:
                calc_move_point()

            move_frame_cnt += 1
            prev_x, prev_y = cur_x, cur_y

    gaze.refresh(frame)
    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_left():
        text = 'left'
        gaze_frame_cnt += 1

    if gaze.is_right():
        text = 'right'
        gaze_frame_cnt += 1

    elif gaze.is_center():
        text = 'center'
        gaze_frame_cnt += 1
        gaze_center += 1

    if gaze_frame_cnt == max_frame_size:
        calc_gaze_point()

    cv2.putText(frame, text, (90, 120), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    cv2.imshow('result', frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27 or k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()