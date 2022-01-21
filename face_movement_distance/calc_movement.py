import csv
import numpy as np
import pandas as pd

result = pd.read_csv('../csv_data/frame100.csv', encoding='utf-8-sig')
result = result.set_index('파일 이름')
idx=result.index

f=open('../csv_data/frame100_movement.csv', 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(f)
writer.writerow(['파일 이름', '이름', 'frame', '이해도 평가', '실제 이해도', 'movement_x', 'movement_y', 'non_detect'])

for cur_idx in idx:
    temp = result.loc[cur_idx]['데이터']
    if type(temp) != str:
        continue
    temp=temp.replace('[', '').replace(', ', ' ')
    temp=temp.split('] ')
    temp.pop()
    non_detect = 0
    move_x=0
    move_y=0
    prev_x= int(temp[0].split(' ')[0])
    prev_y= int(temp[0].split(' ')[1])
    for i in temp[1:]:
        x, y = map(int, i.split(' '))
        if x == 0 and y == 0:
            non_detect+=1
            continue
        move_x += abs(prev_x - x)
        move_y += abs(prev_y - y)
        prev_x=x
        prev_y=y

    res=[cur_idx, result.loc[cur_idx]['이름'], result.loc[cur_idx]['frame'], result.loc[cur_idx]['이해도 평가'],
         result.loc[cur_idx]['실제 이해도'], move_x,
         move_y, non_detect]
    writer.writerow(res)
    # print(res)