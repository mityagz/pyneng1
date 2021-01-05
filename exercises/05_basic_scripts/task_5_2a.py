# -*- coding: utf-8 -*-
"""
Задание 5.2a

Всё, как в задании 5.2, но, если пользователь ввел адрес хоста, а не адрес сети,
надо преобразовать адрес хоста в адрес сети и вывести адрес сети и маску, как в задании 5.2.

Пример адреса сети (все биты хостовой части равны нулю):
* 10.0.1.0/24
* 190.1.0.0/16

Пример адреса хоста:
* 10.0.1.1/24 - хост из сети 10.0.1.0/24
* 10.0.5.195/28 - хост из сети 10.0.5.192/28

Если пользователь ввел адрес 10.0.1.1/24,
вывод должен быть таким:

Network:
10        0         1         0
00001010  00000000  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000

Проверить работу скрипта на разных комбинациях хост/маска, например:
    10.0.5.195/28, 10.0.1.1/24

Подсказка:
Есть адрес хоста в двоичном формате и маска сети 28. Адрес сети это первые 28 бит адреса хоста + 4 ноля.
То есть, например, адрес хоста 10.1.1.195/28  в двоичном формате будет
bin_ip = "00001010000000010000000111000011"

А адрес сети будет первых 28 символов из bin_ip + 0000 (4 потому что всего в адресе может быть 32 бита, а 32 - 28 = 4)
00001010000000010000000111000000

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

prefix = input('Введите префикс x.x.x.x/yy:')

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

print(hostList)
print(bitmaskList)

net_out = "Network:\n{:15}{:15}{:15}{:15}\n{:15}{:15}{:15}{:15}\n"
mask_out = "Mask:\n/{}\n{:<15}{:<15}{:<15}{:<15}\n{:15}{:15}{:15}{:15}\n"

print("Network:\n{:<15}{:<15}{:<15}{:<15}\n{:15}{:15}{:15}{:15}\n".format(int(hostList[0], 2), int(hostList[1], 2), int(hostList[2], 2), int(hostList[3], 2), hostList[0], hostList[1], hostList[2], hostList[3]))
print(mask_out.format(mask, int(bitmaskList[0], 2), int(bitmaskList[1], 2), int(bitmaskList[2], 2), int(bitmaskList[3], 2), bitmaskList[0], bitmaskList[1], bitmaskList[2], bitmaskList[3]))
