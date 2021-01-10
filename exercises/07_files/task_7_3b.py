# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

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
