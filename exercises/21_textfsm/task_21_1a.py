# -*- coding: utf-8 -*-
"""
Задание 21.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM (templates/sh_ip_int_br.template)
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt и шаблоне templates/sh_ip_int_br.template.
"""

from netmiko import ConnectHandler
import textfsm

def do_parse0(tmpl, show_out):
    res = []
    r = []
    with open(tmpl) as t:
        re_table = textfsm.TextFSM(t)
        header = re_table.header
        res = re_table.ParseText(show_out)
        for e in res:
            d = {}
            for i in range(0, len(e)):
               d[header[i]] = e[i]
            r.append(d)
    return r

def do_parse1(tmpl, show_out):
    r = []
    with open(tmpl) as t:
        re_table = textfsm.TextFSM(t)
        header = re_table.header
        res = re_table.ParseText(show_out)
        for e in res:
            r.append(dict(zip(header, e)))
    return r

def do_parse(tmpl, show_out):
    r = []
    with open(tmpl) as t:
        re_table = textfsm.TextFSM(t)
        header = re_table.header
        res = re_table.ParseText(show_out)
        return [ dict(zip(header, e)) for e in res ]

def parse_output_to_dict(tmpl, show_out):
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
    result = parse_output_to_dict("templates/sh_ip_int_br.template", output)
    print(result)
