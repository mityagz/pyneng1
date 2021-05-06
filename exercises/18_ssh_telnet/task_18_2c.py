# -*- coding: utf-8 -*-
"""
Задание 18.2c

Скопировать функцию send_config_commands из задания 18.2b и переделать ее таким образом:

Если при выполнении команды возникла ошибка,
спросить пользователя надо ли выполнять остальные команды.

Варианты ответа [y]/n:
* y - выполнять остальные команды. Это значение по умолчанию, поэтому нажатие любой комбинации воспринимается как y
* n или no - не выполнять остальные команды

Функция send_config_commands по-прежнему должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.

Пример работы функции:

In [11]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: y
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: n

In [12]: pprint(result)
({},
 {'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with '
                        'CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

"""

# списки команд с ошибками и без:
#commands_with_errors = ["logging 0255.255.1", "logging", "a"]
#correct_commands = ["logging buffered 20010", "ip http server"]
commands_with_errors = ["run show interfacu", "run show interfaces yy", "a"]
correct_commands = [ "set system login user cisco1 authentication encrypted-password \"$1$ABzJUPdE$NvSj.G1FVSjPrcZURlgwF0\"", "set system login user cisco1 class super-user" ]

commands = commands_with_errors + correct_commands


import yaml
from netmiko import ConnectHandler
from paramiko.ssh_exception import AuthenticationException
from netmiko.ssh_exception import NetmikoTimeoutException
import re
import sys

def send_config_commands(device, config_commands, log = True):
    d0 = {}
    d1 = {}
    try:
        with ConnectHandler(**device) as ssh:
            if log:
                print("Подключаюсь к {}".format(device['host']))
            for command in config_commands:
                output = ssh.config_mode()
                output += ssh.send_config_set(command)
                ssh.commit()
                isError = False
                for err in [ "syntax error, expecting <command>.", "error: device yy not found", "unknown command.", "is ambiguous.\nPossible completions:" ]:
                    regex = None
                    regex = re.search(err, output)
                    if regex:
                        isError = True
                        break
                if isError:
                    d1[command] = output
                    print("Команда \"{}\" выполнилась с ошибкой \"{}\" на устройстве \"{}\"".format(command, err, device['host']))
                    print("Продолжать выполнять команды? [y]/n:")
                    ans = input()
                    if ans.lower() == "n":
                        sys.exit()
                else:
                    d0[command] = output
                output = ''
            return (d0, d1)
    except (AuthenticationException) as auth_error:
        print(auth_error)
        print("Authentication on {} is fail".format(device['host']))
    except (NetmikoTimeoutException) as timeout_error:
        print(timeout_error)
        print("Connection to {} is fail, timeout raise".format(device['host']))
    except (IOError) as io_err:
        print(io_err)
        print("IOError to {} appeared".format(device['host']))

if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        print(send_config_commands(dev, commands))
