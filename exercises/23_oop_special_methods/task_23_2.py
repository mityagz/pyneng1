# -*- coding: utf-8 -*-

"""
Задание 23.2

Добавить к классу CiscoTelnet из задания 25.2x поддержку работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_23_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка
"""

import telnetlib
import time
from pprint import pprint
import yaml
import sys
import textfsm
from tabulate import tabulate
from textfsm import clitable
import re

pe8_p = {
    'ip': '10.229.10.0',
    'username': 'am',
    'password': 'qwerty',
    'secret': 'qwerty'}

commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
correct_commands = ['logging buffered 20010', 'ip http server']
commands = commands_with_errors + correct_commands


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
            self.telnet = telnetlib.Telnet(ip)
            self.telnet.read_until(b"Username")
            self.ip = ip

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

    def __enter__(self):
            return self

    def __exit__(self, exc_type, exc_value, traceback):
            self.telnet.close()
    
    def _write_line(self, line):
        return self.telnet.write(line.encode("ascii") + b"\n")

    def send_config_commands(self, str_cmd, strict = True):
        self.output = {}
        self.strict = strict
        locmd = []
        if isinstance(str_cmd, str):
            locmd.append(str_cmd)
        else:
            locmd = str_cmd.copy()

        self.send_cmd("conf t")
        for cmd in locmd:
            self.send_cmd(cmd)
        self.send_cmd("end")

        return self.output

    def send_cmd(self, c):
        if self.output.get(c) == None:
            self.output[c] = ''
            res = ''
        self._write_line(c)
        time.sleep(1)
        res = self.telnet.read_very_eager().decode("utf-8")
        self._err(c, res)
        self.output[c] += res

    def _err(self, c, r):
         #m = re.match(r"(?P<detect>%)\s+(?P<err>.*)", r)
         m = re.search(r'% (?P<err>.*)', r)
         if m:
            if("%" in r):
                if self.strict:
                    raise ValueError("При выполнении команды \"{}\" на устройстве {} возникла ошибка -> {}".format(c, self.ip, m.group("err")))
                else:
                    print("При выполнении команды \"{}\" на устройстве {} возникла ошибка -> {}".format(c, self.ip, m.group("err")))

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
        
    with CiscoTelnet(**pe8_p) as pe8:
            print(pe8.send_show_command('sh clock'))

    """
    c = CiscoTelnet(**pe8_p)
    #r = c.send_show_commandis("sh ip int br", parse = True)
    r = c.send_config_commands("logging 10.1.1.1")
    pprint(r, width=120)
    #r = c.send_config_commands("no logging 10.1.1.1")
    #r = c.send_config_commands(['no interface loop55'])
    r = c.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
    pprint(r, width=120)
    r = c.send_config_commands(commands, False)
    pprint(r, width=120)
    r = c.send_config_commands(commands)
    #pprint(r, width=120)
    """
