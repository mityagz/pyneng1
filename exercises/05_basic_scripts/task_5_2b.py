# -*- coding: utf-8 -*-
"""
Задание 5.2b

Преобразовать скрипт из задания 5.2a таким образом,
чтобы сеть/маска не запрашивались у пользователя,
а передавались как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
import sys

#prefix = input('Введите префикс x.x.x.x/yy:')
prefix = sys.argv[1]

net, mask = prefix.split("/")
bitmask=('1' * int(mask)) + ('0' * (32 - int(mask)))

bitmaskList = []
for i in range(0, 32, 8):
    bitmaskList.append(bitmask[i:i + 8])

netList=net.split('.')

netList0 = []
for n in netList:
    netList0.append(str(bin(int(n)).replace('0b', '')))

netList1 = []
for n in netList0:
    netList1.append(('0' * (8 - len(n)) + n))

netList2 = ''.join(netList1)[0:int(mask)] + '0' * (32 - int(mask))

hostList = []
for i in range(0, 32, 8):
    hostList.append(netList2[i:i + 8])

net_out = "Network:\n{:<15}{:<15}{:<15}{:<15}\n{:15}{:15}{:15}{:15}\n"
mask_out = "Mask:\n/{}\n{:<15}{:<15}{:<15}{:<15}\n{:15}{:15}{:15}{:15}\n"

print(net_out.format(int(hostList[0], 2), int(hostList[1], 2), int(hostList[2], 2), int(hostList[3], 2), hostList[0], hostList[1], hostList[2], hostList[3]))
print(mask_out.format(mask, int(bitmaskList[0], 2), int(bitmaskList[1], 2), int(bitmaskList[2], 2), int(bitmaskList[3], 2), bitmaskList[0], bitmaskList[1], bitmaskList[2], bitmaskList[3]))
