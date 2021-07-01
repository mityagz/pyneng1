# -*- coding: utf-8 -*-
"""
Задание 21.1

Создать функцию parse_command_output. Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM (templates/sh_ip_int_br.template)
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список:
* первый элемент - это список с названиями столбцов
* остальные элементы это списки, в котором находятся результаты обработки вывода

Проверить работу функции на выводе команды sh ip int br с оборудования и шаблоне templates/sh_ip_int_br.template.

"""
from netmiko import ConnectHandler
import textfsm

def do_parse(tmpl, show_out):
    with open(tmpl) as t:
        re_table = textfsm.TextFSM(t)
        header = re_table.header
        res = re_table.ParseText(show_out)
        res.insert(0, header)
    return res

def parse_command_output(tmpl, show_out):
    return (do_parse(tmpl, show_out))


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
    result = parse_command_output("templates/sh_ip_int_br.template", output)
    print(result)
