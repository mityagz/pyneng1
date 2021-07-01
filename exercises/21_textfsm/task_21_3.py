# -*- coding: utf-8 -*-
"""
Задание 21.3

Создать функцию parse_command_dynamic.

Параметры функции:
* command_output - вывод команды (строка)
* attributes_dict - словарь атрибутов, в котором находятся такие пары ключ-значение:
 * 'Command': команда
 * 'Vendor': вендор
* index_file - имя файла, где хранится соответствие между командами и шаблонами. Значение по умолчанию - "index"
* templ_path - каталог, где хранятся шаблоны. Значение по умолчанию - "templates"

Функция должна возвращать список словарей с результатами обработки вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br.
"""


from netmiko import ConnectHandler
import textfsm
from textfsm import clitable
import task_21_1a as h

#cisco_ios, sh[[ow]] ip int[[erface]] br[[ief]
attributes_dict = {'Command': 'show ip interface brief', 'Vendor': 'cisco_ios'}

def parse_command_dynamic(command_output, attributes_dict, index_file = 'index', templ_path = 'templates'):
    ct = clitable.CliTable(index_file, templ_path)
    ct.ParseCmd(command_output, attributes_dict)
    header = (ct.header)
    return [ dict(zip(header, e)) for e in ct ]

# вызов функции должен выглядеть так
if __name__ == "__main__":
    r1_params = {
        "device_type": "cisco_ios",
        "host": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    #with ConnectHandler(**r1_params) as r1:
        #r1.enable()
        #output = r1.send_command("sh ip int br")
    with open("output/sh_ip_int_br.txt") as f, open("output/sh_ip_int_br.txt") as output:
     output = f.read()
     result = parse_command_dynamic(output, attributes_dict)
    print(result)
