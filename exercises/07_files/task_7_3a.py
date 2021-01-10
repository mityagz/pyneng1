# -*- coding: utf-8 -*-
"""
Задание 7.3a

Сделать копию скрипта задания 7.3.

Дополнить скрипт:
- Отсортировать вывод по номеру VLAN

В результате должен получиться такой вывод:
10       01ab.c5d0.70d0      Gi0/8
10       0a1b.1c80.7000      Gi0/4
100      01bb.c580.7000      Gi0/1
200      0a4b.c380.7c00      Gi0/2
200      1a4b.c580.7000      Gi0/6
300      0a1b.5c80.70f0      Gi0/7
300      a2ab.c5a0.700e      Gi0/3
500      02b1.3c80.7b00      Gi0/5
1000     0a4b.c380.7d00      Gi0/9

Обратите внимание на vlan 1000 - он должен выводиться последним.
Правильной сортировки можно добиться, если vlan будет числом, а не строкой.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

import sys

cam = {}
keys = []

with open(sys.argv[1], 'r') as f_cam:
    for l in f_cam:
        if l.find('DYNAMIC') != -1:
            al0 = l.split()
            cam_k = int(al0[0])
            if cam.get(cam_k):
                cam[cam_k].append([al0[1], al0[3]])
            else:
                cam[cam_k] = []
                cam[cam_k].append([al0[1], al0[3]])


for k in cam:
    keys.append(k)

keys.sort()

vid = input('Enter vlan or vlan list:')
vid_list = vid.split(',')

for k in keys:
    for l in cam[k]:
        for vid_l in vid_list:
            if int(vid_l) == k:
                #print(k, l[0], l[1], cam[k])
                print(k, l[0], l[1])
