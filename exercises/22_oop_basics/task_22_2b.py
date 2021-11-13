# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko (пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

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

    def send_config_command(self, str_cmd):
        self.output = ''
        self.send_cmd("conf t\n")
        
        if isinstance(str_cmd, str):
            self.send_cmd(str_cmd)
        else:
            for cmd in str_cmd:
                self.send_cmd(cmd)
        
        self.send_cmd("end\n")
        return self.output

    def send_cmd(self, c):
        self.output += self.telnet.read_until(b"#", timeout=3).decode("utf-8")
        self._write_line(c)
        self.output += self.telnet.read_until(b"#", timeout=3).decode("utf-8")

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
    #r = c.send_show_command("sh ip int br", parse = True)
    r = c.send_config_command("logging 10.1.1.1")
    pprint(r, width=120)
    #r = c.send_config_command("no logging 10.1.1.1")
    #r = c.send_config_command(['no interface loop55'])
    r = c.send_config_command(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
    pprint(r, width=120)
