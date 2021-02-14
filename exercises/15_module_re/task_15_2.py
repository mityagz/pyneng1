# -*- coding: utf-8 -*-
"""
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            15.0.15.1       YES manual up                    up
FastEthernet0/1            10.0.12.1       YES manual up                    up
FastEthernet0/2            10.0.13.1       YES manual up                    up
FastEthernet0/3            unassigned      YES unset  administratively down down
Loopback0                  10.1.1.1        YES manual up                    up
Loopback100                100.0.0.1       YES manual up                    up


"""
import re

def parse_sh_ip_int_br(fname):
    result = []
    with open(fname, 'r') as fd:
        conf = fd.read()
        regexp = (r'(?P<intf>\S+)\s+(?P<ip>(\d{1,3}\.){3}\d{1,3}|unassigned)\s+\w+\s+\w+\s+(?P<status>up|down|administratively down)\s+(?P<proto>up|down)')
        iter = re.finditer(regexp, conf)
        for i in iter:
            result.append(i.group('intf', 'ip', 'status', 'proto'))
    return result




if __name__ == '__main__':
    print(parse_sh_ip_int_br('sh_ip_int_br.txt'))
