# -*- coding: utf-8 -*-
"""
Задание 18.1a

Скопировать функцию send_show_command из задания 18.1 и переделать ее таким образом,
чтобы обрабатывалось исключение, которое генерируется
при ошибке аутентификации на устройстве.

При возникновении ошибки, на стандартный поток вывода должно выводиться сообщение исключения.

Для проверки измените пароль на устройстве или в файле devices.yaml.
"""

import yaml
from netmiko import ConnectHandler
from paramiko.ssh_exception import AuthenticationException
#from paramiko.ssh_exception import TimeoutException

def send_show_command(device, command):
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            output = ssh.send_command(command)
            return output
    except (AuthenticationException) as auth_error:
        print(auth_error)
        print("Authentication on {} is fail".format(device['host']))
    #except (TimeoutException) as timeout_error:
        #print(error)
        #print("Connection to {} is fail, timeout raise".format(device))


if __name__ == "__main__":
    command = "show interfaces brief"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        print(send_show_command(dev, command))
