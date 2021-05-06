# -*- coding: utf-8 -*-
"""
Задание 18.3

Создать функцию send_commands (для подключения по SSH используется netmiko).

Параметры функции:
* device - словарь с параметрами подключения к одному устройству, которому надо передать команды
* show - одна команда show (строка)
* config - список с командами, которые надо выполнить в конфигурационном режиме

В зависимости от того, какой аргумент был передан, функция вызывает разные функции внутри.
При вызове функции send_commands, всегда будет передаваться только один из аргументов show, config.

Далее комбинация из аргумента и соответствующей функции:
* show - функция send_show_command из задания 19.1
* config - функция send_config_commands из задания 19.2

Функция возвращает строку с результатами выполнения команд или команды.

Проверить работу функции:
* со списком команд commands
* командой command

Пример работы функции:

In [14]: send_commands(r1, show='sh clock')
Out[14]: '*17:06:12.278 UTC Wed Mar 13 2019'

In [15]: send_commands(r1, config=['username user5 password pass5', 'username user6 password pass6'])
Out[15]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#username user5 password pass5\nR1(config)#username user6 password pass6\nR1(config)#end\nR1#'
"""

#commands = ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]
#command = "sh ip int br"

import task_18_1 as c0
import task_18_2 as c1
import yaml


commands = [ "set system login user cisco1 authentication encrypted-password \"$1$ABzJUPdE$NvSj.G1FVSjPrcZURlgwF0\"", "set system login user cisco1 class super-user" ]
command = "show interfaces brief"

def send_commands(device, *, show = None, config = None):
    if show != None and config != None:
        raise ValueError()
    elif show != None:
        return c0.send_show_command(device, show)
    else:
        return c1.send_config_commands(device, config)

if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    command = "show interfaces brief"

    #print(send_commands(devices[0], show=command, config=commands))
    print(send_commands(devices[0], show=command))
    print(send_commands(devices[0], config=commands))
