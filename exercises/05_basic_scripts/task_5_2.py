# -*- coding: utf-8 -*-
"""
Задание 5.2

Запросить у пользователя ввод IP-сети в формате: 10.1.1.0/24

Затем вывести информацию о сети и маске в таком формате:

Network:
10        1         1         0
00001010  00000001  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000

Проверить работу скрипта на разных комбинациях сеть/маска.

Подсказка: Получить маску в двоичном формате можно так:
In [1]: "1" * 28 + "0" * 4
Out[1]: '11111111111111111111111111110000'


Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

prefix = input('Введите префикс x.x.x.x/yy:')

net = prefix.split("/")[0]
mask = prefix.split("/")[1]

print(net, mask)


n0 = net.split(".")[0]
n1 = net.split(".")[1]
n2 = net.split(".")[2]
n3 = net.split(".")[3]


################### Net
netbin3 = bin(int(n0)).replace("0b", "")
netbin2 = bin(int(n1)).replace("0b", "")
netbin1 = bin(int(n2)).replace("0b", "")
netbin0 = bin(int(n3)).replace("0b", "")

netbin3 = "0" * (8 - len(netbin3)) + netbin3
netbin2 = "0" * (8 - len(netbin2)) + netbin2
netbin1 = "0" * (8 - len(netbin1)) + netbin1
netbin0 = "0" * (8 - len(netbin0)) + netbin0

################### Mask
mask1 = 32 - int(mask)
maskbin = "1" * int(mask) + "0" * mask1

maskbin3 = maskbin[0:8]
maskbin2 = maskbin[8:16]
maskbin1 = maskbin[16:24]
maskbin0 = maskbin[24:32]

maskdec3 = int(maskbin3, 2)
maskdec2 = int(maskbin2, 2)
maskdec1 = int(maskbin1, 2)
maskdec0 = int(maskbin0, 2)

print("Network:\n{:15}{:15}{:15}{:15}\n{:15}{:15}{:15}{:15}\n".format(n0, n1, n2, n3, netbin3, netbin2, netbin1, netbin0))
print("Mask:\n/{}\n{:<15}{:<15}{:<15}{:<15}\n{:15}{:15}{:15}{:15}\n".format(mask, maskdec3, maskdec2, maskdec1, maskdec0, maskbin3, maskbin2, maskbin1, maskbin0))
