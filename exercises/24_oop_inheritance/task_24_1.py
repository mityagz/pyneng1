# -*- coding: utf-8 -*-

"""
Задание 24.1

Создать класс CiscoSSH, который наследует класс BaseSSH из файла base_connect_class.py.

Создать метод __init__ в классе CiscoSSH таким образом, чтобы после подключения по SSH выполнялся переход в режим enable.

Для этого в методе __init__ должен сначала вызываться метод __init__ класса BaseSSH, а затем выполняться переход в режим enable.

In [2]: from task_24_1 import CiscoSSH

In [3]: r1 = CiscoSSH(**device_params)

In [4]: r1.send_show_command('sh ip int br')
Out[4]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

"""

device_params = {
    "device_type": "cisco_ios",
    "ip": "10.229.10.0",
    "username": "am",
    "password": "qwerty",
    "secret": "cisco",
}

from base_connect_class import BaseSSH

class CiscoSSH(BaseSSH):
    def __init__(self, device_type, ip, username, password, secret, disable_paging=True):
            super().__init__(**device_params)
            self.ssh.enable()
            #if disable_paging:
            #    self.send_cfg_commands('terminal length 0\n')
            #time.sleep(1)

if __name__ == '__main__':
    r = CiscoSSH(**device_params)
    print(r.send_show_command('sh ip int br'))
