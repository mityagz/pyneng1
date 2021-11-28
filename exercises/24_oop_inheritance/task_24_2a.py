# -*- coding: utf-8 -*-

"""
Задание 24.2a

Дополнить класс MyNetmiko из задания 24.2.

Добавить метод _check_error_in_command, который выполняет проверку на такие ошибки:
 * Invalid input detected, Incomplete command, Ambiguous command

Метод ожидает как аргумент команду и вывод команды.
Если в выводе не обнаружена ошибка, метод ничего не возвращает.
Если в выводе найдена ошибка, метод должен генерировать исключение ErrorInCommand с сообщением о том какая ошибка была обнаружена, на каком устройстве и в какой команде.

Исключение ErrorInCommand создано в файле задания.

Переписать метод send_command netmiko, добавив в него проверку на ошибки.

In [2]: from task_24_2a import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_command('sh ip int br')
Out[4]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

In [5]: r1.send_command('sh ip br')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-1c60b31812fd> in <module>()
----> 1 r1.send_command('sh ip br')
...
ErrorInCommand: При выполнении команды "sh ip br" на устройстве 192.168.100.1 возникла ошибка "Invalid input detected at '^' marker."

"""


class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании, возникла ошибка.
    """

from netmiko.cisco.cisco_ios import CiscoIosSSH
import re


device_params = {
    "device_type": "cisco_ios",
    "ip": "10.229.10.0",
    "username": "am",
    "password": "qwerty",
    "secret": "cisco",
}



class MyNetmiko(CiscoIosSSH):
    #def __init__(self, device_type, ip, username, password, secret, disable_paging = True):
    def __init__(self, **device_params):
        self.dev_ip = device_params['ip']
        super().__init__(**device_params)
        self.enable()


    def _check_error_in_command(self, cmd, ocmd):
            regex = None
            err = r'% (?P<err>.*)'
            regex = re.search(err, ocmd)
            if regex:
                excn = "При выполнении команды \"{}\" на устройстве {} возникла ошибка {}".format(cmd, self.dev_ip, regex.group('err'))
                raise ErrorInCommand(excn)

    def send_command(self, cmd):
        ocmd = super().send_command(cmd)
        if cmd == 'logging':
            ocmd = super().send_config_set(cmd)
        self._check_error_in_command(cmd, ocmd)
        return ocmd

if __name__ == '__main__':
    r = MyNetmiko(**device_params)
    print(r.send_command('sh ip int br'))
    print(r.send_command('sh ip br'))
