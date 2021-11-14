# -*- coding: utf-8 -*-

"""
Задание 22.2c

Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set у netmiko (пример вывода ниже).
Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

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
