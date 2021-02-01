# -*- coding: utf-8 -*-
"""
Задание 12.3


Создать функцию print_ip_table, которая отображает таблицу доступных и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

Функция не должна изменять списки, которые переданы ей как аргументы.
То есть, до выполнения функции и после списки должны выглядеть одинаково.


Для этого задания нет тестов
"""

from task_12_2 import convert_ranges_to_ip_list
from task_12_1  import ping_ip_addresses
from tabulate import tabulate

def print_ip_table(ip_list):
    ips = convert_ranges_to_ip_list(ip_list)
    ip_alive = ping_ip_addresses(ips)

    d = len(ip_alive[0]) - len(ip_alive[1])
    if d > 0:
        [ ip_alive[1].append('') for x in range(0, d)]
    elif d < 0:
        [ ip_alive[0].append('') for x in range(d, 0)]

    columns=[ 'Reachable', 'Unreachable' ]
    print(tabulate(zip(ip_alive[0], ip_alive[1]), headers=columns))
    return(ip_alive)


if __name__ == '__main__':
    ipl = [ '8.8.8.8', '8.8.4.4', '10.1.11.8-25', '60.128.224.10-60.128.224.15' ]
    print(print_ip_table(ipl))
