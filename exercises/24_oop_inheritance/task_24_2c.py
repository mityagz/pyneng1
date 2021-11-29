# -*- coding: utf-8 -*-

"""
Задание 24.2c

Проверить, что метод send_command класса MyNetmiko из задания 24.2b, принимает дополнительные аргументы (как в netmiko), кроме команды.

Если возникает ошибка, переделать метод таким образом, чтобы он принимал любые аргументы, которые поддерживает netmiko.


In [2]: from task_24_2c import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_command('sh ip int br', strip_command=False)
Out[4]: 'sh ip int br\nInterface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

In [5]: r1.send_command('sh ip int br', strip_command=True)
Out[5]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

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

    def send_command(self, *args, **kwargs):
        cmd = args
        ocmd = super().send_command(*args, **kwargs)
        if cmd == 'logging':
            ocmd = super().send_config_set(cmd)
        self._check_error_in_command(*args, ocmd)
        return ocmd

    def send_config_set(self, cmd):
        ocmd = super().send_config_set(cmd)
        self._check_error_in_command(cmd, ocmd)
        return ocmd

if __name__ == '__main__':
    r = MyNetmiko(**device_params)
    print(r.send_command('sh ip int br'))
    print(r.send_command('sh ip br'))
