# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

import subprocess

def ping_ip_addresses(ip_list):
    a = []
    ua = []
    for ip in ip_list:
        ret = subprocess.run('ping -c 1 {}'.format(ip), shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        if ret.returncode == 0:
            a.append(ip)
        else:
            ua.append(ip)
    return a, ua


if __name__ == '__main__':
    print(ping_ip_addresses([ '8.8.8.8', '65.65.65.65', '8.8.4.4' ]))
