# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0
SW1              Eth 0/0            131          S I      WS-C3750- Eth 0/3

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""

import re

def parse_sh_cdp_neighbors(sh_cdp_nei):
    res = {}
    m0 = re.search(r'(?P<lhost>\S+)>show cdp neighbors', sh_cdp_nei)
    m1 = re.finditer(r'(?P<rhost>\S+)\s+(?P<lintf>\w+ \S+)\s+\d+.*[\d+|\S+]\s+(?P<rintf>\w+ \S+)', sh_cdp_nei)
    if m0 and m1:
        lhost = m0.group('lhost')
        for m in m1:
            if res.get(m0.group('lhost')) == None:
                res[m0.group('lhost')] = {}
            if res.get(m0.group('lhost')).get(m.group('lintf')) == None:
                res[m0.group('lhost')][m.group('lintf')] = {}
                res[m0.group('lhost')][m.group('lintf')][m.group('rhost')] = m.group('rintf')
    return(res)


if __name__ == '__main__':
    with open('sh_cdp_n_sw1.txt', 'r') as f:
        sh = f.read()
        print(parse_sh_cdp_neighbors(sh))
