# -*- coding: utf-8 -*-
"""
Задание 18.2b

Скопировать функцию send_config_commands из задания 18.2a и добавить проверку на ошибки.

При выполнении каждой команды, скрипт должен проверять результат на такие ошибки:
 * Invalid input detected, Incomplete command, Ambiguous command

Если при выполнении какой-то из команд возникла ошибка,
функция должна выводить сообщение на стандартный поток вывода с информацией
о том, какая ошибка возникла, при выполнении какой команды и на каком устройстве, например:
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1

Ошибки должны выводиться всегда, независимо от значения параметра log.
При этом, параметр log по-прежнему должен контролировать будет ли выводиться сообщение:
Подключаюсь к 192.168.100.1...


Функция send_config_commands теперь должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате (примеры словарей ниже):
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.


Пример работы функции send_config_commands:

In [16]: commands
Out[16]:
['logging 0255.255.1',
 'logging',
 'a',
 'logging buffered 20010',
 'ip http server']

In [17]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Команда "a" выполнилась с ошибкой "Ambiguous command:  "a"" на устройстве 192.168.100.1

In [18]: pprint(result, width=120)
({'ip http server': 'config term\n'
                    'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                    'R1(config)#ip http server\n'
                    'R1(config)#',
  'logging buffered 20010': 'config term\n'
                            'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                            'R1(config)#logging buffered 20010\n'
                            'R1(config)#'},
 {'a': 'config term\n'
       'Enter configuration commands, one per line.  End with CNTL/Z.\n'
       'R1(config)#a\n'
       '% Ambiguous command:  "a"\n'
       'R1(config)#',
  'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

In [19]: good, bad = result

In [20]: good.keys()
Out[20]: dict_keys(['logging buffered 20010', 'ip http server'])

In [21]: bad.keys()
Out[21]: dict_keys(['logging 0255.255.1', 'logging', 'a'])


Примеры команд с ошибками:
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"

am@CE1> show interfacu    
             ^
syntax error, expecting <command>.
am@CE1> show interfaces yy 
error: device yy not found

am@CE1> a
        ^
unknown command.
am@CE1> 

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
                if isError:
                    d1[command] = output
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
