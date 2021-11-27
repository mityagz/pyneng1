# -*- coding: utf-8 -*-

"""
Задание 24.1a

Дополнить класс CiscoSSH из задания 24.1.

Перед подключением по SSH необходимо проверить если ли в словаре
с параметрами подключения такие параметры: username, password, secret.
Если нет, запросить их у пользователя, а затем выполнять подключение.
Если параметры есть, сразу выполнить подключение.

In [1]: from task_24_1a import CiscoSSH

In [2]: device_params = {
   ...:         'device_type': 'cisco_ios',
   ...:         'host': '192.168.100.1',
   ...: }

In [3]: r1 = CiscoSSH(**device_params)
Введите имя пользователя: cisco
Введите пароль: cisco
Введите пароль для режима enable: cisco

In [4]: r1.send_show_command('sh ip int br')
Out[4]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

"""

device_params = { "device_type": "cisco_ios", "host": "10.229.10.0" }

"""
device_params = {
    "device_type": "cisco_ios",
    "ip": "10.229.10.0",
    "username": "am",
    "password": "qwerty",
    "secret": "cisco",
}
"""


from base_connect_class import BaseSSH

class CiscoSSH(BaseSSH):
    #def __init__(self, device_type, ip, username, password, secret, disable_paging = True):
    def __init__(self, **device_params):
            check_params(device_params)
            super().__init__(**device_params)
            self.ssh.enable()
            #super().send_cfg_commands('enable\n')
            #super().send_cfg_commands(secret + '\n')
            #if disable_paging:
            #    self.send_cfg_commands('terminal length 0\n')
            #time.sleep(1)
    

    """
    def _modify_connection_params(self): 
            paramiko.Transport._preferred_kex = ( 
                "diffie-hellman-group14-sha1", 
                "diffie-hellman-group-exchange-sha1", 
                "diffie-hellman-group-exchange-sha256", 
                "diffie-hellman-group1-sha1", 
                ) 

    def _open(self):
            self._modify_connection_params()
            self.establish_connection()
            self._try_session_preparation()
    """
def check_params(device_params):
    for y in [ { 'device_type': 'Введите тип устройства:' }, { 'ip' : 'Введите ip:' }, { 'username' : 'Введите имя пользователя:' }, { 'password' : 'Введите пароль:' }, { 'secret' : 'Введите пароль для режима enable:' } ]:
        itm = list(y.items())
        if device_params.get(itm[0][0]) == None:
            print(itm[0][1], end = '')
            v = input()
            device_params[itm[0][0]] = v

if __name__ == '__main__':
    r = CiscoSSH(**device_params)
    print(r.send_show_command('sh ip int br'))
