# -*- coding: utf-8 -*-
"""
Задание 21.2

Сделать шаблон TextFSM для обработки вывода sh ip dhcp snooping binding и записать его в файл templates/sh_ip_dhcp_snooping.template

Вывод команды находится в файле output/sh_ip_dhcp_snooping.txt.

Шаблон должен обрабатывать и возвращать значения таких столбцов:
* mac - такого вида 00:04:A3:3E:5B:69
* ip - такого вида 10.1.10.6
* vlan - 10
* intf - FastEthernet0/10

Проверить работу шаблона с помощью функции parse_command_output из задания 21.1.
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
    with open("output/sh_ip_dhcp_snooping.txt") as f:
     output = f.read()
    result = parse_command_output("templates/sh_ip_dhcp_snooping.template", output)
    print(result)

"""
#00:09:BB:3D:D6:58   10.1.10.2        86250       dhcp-snooping   10    FastEthernet0/1
Value mac (([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))
Value ip (((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))
Value vlan (\d{1,4})
Value intf (\S+)

Start
  ^${mac}\s+${ip}\s+\d+\s+\S+\s+${vlan}\s+${intf} -> Record

"""
