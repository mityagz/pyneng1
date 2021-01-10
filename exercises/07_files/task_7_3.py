# -*- coding: utf-8 -*-
"""
Задание 7.3

Скрипт должен обрабатывать записи в файле CAM_table.txt.
Каждая строка, где есть MAC-адрес, должна быть обработана таким образом,
чтобы на стандартный поток вывода была выведена таблица вида (показаны не все строки из файла):

 100    01bb.c580.7000   Gi0/1
 200    0a4b.c380.7000   Gi0/2
 300    a2ab.c5a0.7000   Gi0/3
 100    0a1b.1c80.7000   Gi0/4
 500    02b1.3c80.7000   Gi0/5
 200    1a4b.c580.7000   Gi0/6
 300    0a1b.5c80.7000   Gi0/7

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
