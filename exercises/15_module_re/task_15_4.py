# -*- coding: utf-8 -*-
"""
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.


Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
"""

import re

def get_ints_without_description(fcfg):
    r = []
    regexp0 = (r'^interface\s+(?P<intf>\S+)')
    regexp1 = (r'description\s+(?P<desc>.*)')
    with open(fcfg, 'r') as f:
        conf = f.read().split('\n')
        for i in range(0, len(conf)):
            match0 = re.search(regexp0, conf[i])
            if match0:
                match1 = re.search(regexp1, conf[i + 1])
                if not match1:
                    r.append(match0.group('intf'))
    return r

if __name__ == '__main__':
    print(get_ints_without_description('config_r1.txt'))
