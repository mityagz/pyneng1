# -*- coding: utf-8 -*-

"""
Задание 22.2a

Скопировать класс CiscoTelnet из задания 22.2 и изменить метод send_show_command добавив три параметра:

* parse - контролирует то, будет возвращаться обычный вывод команды или список словарей, полученные после обработки с помощью TextFSM. При parse=True должен возвращаться список словарей, а parse=False обычный вывод. Значение по умолчанию - True.
* templates - путь к каталогу с шаблонами. Значение по умолчанию - "templates"
* index - имя файла, где хранится соответствие между командами и шаблонами. Значение по умолчанию - "index"


Пример создания экземпляра класса:

In [1]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [2]: from task_22_2a import CiscoTelnet

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_show_command:
In [4]: r1.send_show_command("sh ip int br", parse=True)
Out[4]:
[{'intf': 'Ethernet0/0',
  'address': '192.168.100.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/1',
  'address': '192.168.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/2',
  'address': '192.168.130.1',
  'status': 'up',
  'protocol': 'up'}]

In [5]: r1.send_show_command("sh ip int br", parse=False)
Out[5]: 'sh ip int br | exclude unassigned\r\nInterface                  IP-Address      OK? Method Status                Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \r\nEthernet0/2                192.168.130.1   YES NVRAM  up                    up      \r\n\r\nR1#'


"""


import telnetlib
import time
from pprint import pprint
import yaml
import sys
import textfsm
from tabulate import tabulate
from textfsm import clitable

pe8_p = {
    'ip': '10.229.10.0',
    'username': 'am',
    'password': 'qwerty',
    'secret': 'qwerty'}

class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
            self.telnet = telnetlib.Telnet(ip)
            self.telnet.read_until(b"Username")

            self._write_line(username)
            self.telnet.read_until(b"Password")
            self._write_line(password)
            index, m, output = self.telnet.expect([b">", b"#"])
            if index == 0:
                #self.telnet.write(b"enable\n")
                self._write_line("enable")
                self.telnet.read_until(b"Password")
                self._write_line(secret)
                self.telnet.read_until(b"#", timeout=5)
                self._write_line("terminal length 0")
                self.telnet.read_until(b"#", timeout=5)
                time.sleep(3)
                self.telnet.read_very_eager()
    
    def _write_line(self, line):
        return self.telnet.write(line.encode("ascii") + b"\n")

    def send_show_command(self, str_cmd, parse = False, templates = 'templates', index = 'index'):
        r = {}
        self._write_line(str_cmd)
        if not parse:
            output = self.telnet.read_until(b"#", timeout=5).decode("utf-8")
            return output
        else:
            result = []
            cli_table = clitable.CliTable('index', 'templates')
            attributes = {'Command': 'show ip interface brief', 'Vendor': 'Cisco'}
            output = self.telnet.read_until(b"#", timeout=5).decode("utf-8")
            cli_table.ParseCmd(output, attributes)
            result = [ dict(zip(cli_table.header, v)) for v in [ list(row) for row in cli_table ] ]
            """
            for ll in data_rows:
                d = {}
                for idx, v in enumerate(ll):
                        d[cli_table.header[idx]] = v
                result.append(d)
            """
            #result = [ dict(zip(cli_table.header, v)) for v in data_rows ]
            return result

if __name__ == '__main__':
    c = CiscoTelnet(**pe8_p)
    r = c.send_show_command("sh ip int br", parse = True)
    pprint(r, width=120)
