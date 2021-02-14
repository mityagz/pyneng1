# -*- coding: utf-8 -*-
"""
Задание 15.1b

Проверить работу функции get_ip_from_cfg из задания 15.1a на конфигурации config_r2.txt.

Обратите внимание, что на интерфейсе e0/1 назначены два IP-адреса:
interface Ethernet0/1
 ip address 10.255.2.2 255.255.255.0
 ip address 10.254.2.2 255.255.255.0 secondary

А в словаре, который возвращает функция get_ip_from_cfg, интерфейсу Ethernet0/1
соответствует только один из них (второй).

Скопировать функцию get_ip_from_cfg из задания 15.1a и переделать ее таким образом,
чтобы в значении словаря она возвращала список кортежей для каждого интерфейса.
Если на интерфейсе назначен только один адрес, в списке будет один кортеж.
Если же на интерфейсе настроены несколько IP-адресов, то в списке будет несколько кортежей.
Ключом остается имя интерфейса.

Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу
Ethernet0/1 соответствует список из двух кортежей.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

"""

import re

def get_ip_from_cfg(conf_file):
    result = {}
    regex = re.compile(r'interface (?P<intf>\S+)\n'
                       r'( description.*\n)?( bandwidth \d+\n)? '
                       r'(?:ip address (?P<ip>\S+) (?P<mask>\S+)\n)'
                       r'(?: ip address (?P<ip_sec>\S+) (?P<mask_sec>\S+) secondary\n)?')

    with open(conf_file, 'r') as f:
        conf = f.read()
        match_iter = regex.finditer(conf)
        for match in match_iter:
            result[match.group('intf')] =  []
            result[match.group('intf')].append(match.group('ip', 'mask'))
            if match.group('ip_sec') != None:
                result[match.group('intf')].append(match.group('ip_sec', 'mask_sec'))
            print(match.groups())
    return result

def get_ip_from_cfg0(conf_file):
    result = {}
    regex = re.compile(r'^interface (?P<intf>\S+)|(?: ip address (?P<ip>\S+) (?P<mask>\S+))')

    with open(conf_file, 'r') as f:
        for l in f:
            match = regex.search(l)
            if match:
                if match.lastgroup == 'intf':
                    intf = match.group('intf')
                if match.lastgroup == 'mask':
                    if result.get(intf) ==  None:
                        result[intf] = []
                    ip, mask = match.group('ip', 'mask')
                    result[intf].append((ip, mask))
    return result

if __name__ == '__main__':
    print(get_ip_from_cfg('config_r2.txt'))
