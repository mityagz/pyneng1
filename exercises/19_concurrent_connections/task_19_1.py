# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""

from concurrent.futures import ThreadPoolExecutor
from pprint import pprint
from datetime import datetime
import time
import subprocess
from itertools import repeat
import logging

def ping_ip_addresses(ip_list, limit=3):
    a = []
    ua = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
            result = executor.map(ping_ip, ip_list)
            for ip, res in zip(ip_list, result):
                if res == 0:
                    a.append(ip)
                else:
                    ua.append(ip)
    return (a, ua)


def ping_ip(ip):
    ret = None
    try:
        ret = subprocess.run('ping -c 1 {}'.format(ip), shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', timeout=1)
        return ret.returncode
    except subprocess.TimeoutExpired:
        print("Timeout was appeared while was executing ping to {}".format(ip))
        return 1
    return 1

if __name__ == '__main__':
    pprint(ping_ip_addresses([ '8.8.8.8', '8.8.4.4', '8.8.8.89', '127.0.0.2' ], 3))
