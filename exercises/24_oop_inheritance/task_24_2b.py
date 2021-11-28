# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

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

    def send_config_set(self, cmd):
        ocmd = super().send_config_set(cmd)
        self._check_error_in_command(cmd, ocmd)
        return ocmd

if __name__ == '__main__':
    r = MyNetmiko(**device_params)
    print(r.send_command('sh ip int br'))
    print(r.send_command('sh ip br'))
