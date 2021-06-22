# -*- coding: utf-8 -*-
"""
Задание 19.4

Создать функцию send_commands_to_devices, которая отправляет команду show или config на разные устройства в параллельных потоках, а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* show - команда show, которую нужно отправить (по умолчанию, значение None)
* config - команды конфигурационного режима, которые нужно отправить (по умолчанию, значение None)
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Пример вызова функции:
In [5]: send_commands_to_devices(devices, show='sh clock', filename='result.txt')

In [6]: cat result.txt
R1#sh clock
*04:56:34.668 UTC Sat Mar 23 2019
R2#sh clock
*04:56:34.687 UTC Sat Mar 23 2019
R3#sh clock
*04:56:40.354 UTC Sat Mar 23 2019

In [11]: send_commands_to_devices(devices, config='logging 10.5.5.5', filename='result.txt')

In [12]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 10.5.5.5
R1(config)#end
R1#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#logging 10.5.5.5
R2(config)#end
R2#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#logging 10.5.5.5
R3(config)#end
R3#

In [13]: send_commands_to_devices(devices,
                                  config=['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0'],
                                  filename='result.txt')

In [14]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#router ospf 55
R1(config-router)#network 0.0.0.0 255.255.255.255 area 0
R1(config-router)#end
R1#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#router ospf 55
R2(config-router)#network 0.0.0.0 255.255.255.255 area 0
R2(config-router)#end
R2#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#router ospf 55
R3(config-router)#network 0.0.0.0 255.255.255.255 area 0
R3(config-router)#end
R3#


Для выполнения задания можно создавать любые дополнительные функции.
"""

# Этот словарь нужен только для проверки работа кода, в нем можно менять IP-адреса
# тест берет адреса из файла devices.yaml
commands = {
    "10.240.0.65": [ "show configuration protocols ospf", "show configuration protocols lldp" ],
    "10.240.0.66": [ "show interfaces brief", "show configuration protocols lldp" ],
    "10.248.0.65": [ "show interfaces descriptions" ],
    "10.248.0.66": [ "show interfaces descriptions", "show configuration protocols lldp" ],
}

commands_config = [ "set system login user cisco1 authentication encrypted-password \"$1$ABzJUPdE$NvSj.G1FVSjPrcZURlgwF0\"", "set system login user cisco1 class super-user" ]


from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
from datetime import datetime
import time
from itertools import repeat
import logging

import yaml
from netmiko import ConnectHandler


from paramiko.ssh_exception import AuthenticationException
from netmiko.ssh_exception import NetmikoTimeoutException, NetMikoAuthenticationException

logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)

start_msg = '===> {} Connection: {}'
received_msg = '<=== {} Received: {}'

def send_show_commands(device_dict, command):
    ip = device_dict['ip']
    print(ip, command)
    logging.info(start_msg.format(datetime.now().time(), ip))
    with ConnectHandler(**device_dict) as ssh:
        prompt = ssh.find_prompt()
        ssh.write_channel(f"{command}\n")
        #output = prompt + command
        output = ""
        while True:
            try:
                page = ssh.read_until_pattern(f"More|{prompt}")
                output += page
                if "More" in page:
                    ssh.write_channel(" ")
                elif prompt in output:
                    break
            except NetmikoTimeoutException:
                    break
    logging.info(received_msg.format(datetime.now().time(), ip))
    return {ip: output}

def send_config_commands(device, config_commands):
    result = {}
    output = ""
    ip = device['ip']
    logging.info(start_msg.format(datetime.now().time(), ip))
    try:
        with ConnectHandler(**device) as ssh:
            output = ssh.config_mode()
            output += ssh.send_config_set(config_commands)
            ssh.commit()
            logging.info(received_msg.format(datetime.now().time(), ip))
            return {ip: output}
    except (AuthenticationException) as auth_error:
        print(auth_error)
        print("Authentication on {} is fail".format(device['host']))
    except (NetmikoTimeoutException) as timeout_error:
        print(timeout_error)
        print("Connection to {} is fail, timeout raise".format(device['host']))
    except (IOError) as io_err:
        print(io_err)
        print("IOError to {} appeared".format(device['host']))
        return {ip: output}


def send_commands_to_devices(devices, filename, limit = 3, *, show = None, config = None):
    data = {}
    data_e = {}
    log = []
    futures_ssh = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        if show != None and config != None:
            raise ValueError()
        elif show != None:
            print([ "{} {}".format(device['ip'], c) for device in devices for c in commands[device['ip']]])
            futures_ssh = [ executor.submit(send_show_commands, device, c) for device in devices for c in commands[device['ip']] ]
        else:
            print([ "{} {}".format(device['ip'], c) for device in devices for c in commands_config ])
            futures_ssh = [ executor.submit(send_config_commands, device, config) for device in devices ]

        for f in as_completed(futures_ssh):
            try:
                result = f.result()
            except NetMikoAuthenticationException as e:
                print(e)
            else:
                ip_dev = ((list(result.keys()))[0])
                out_val = ((list(result.values()))[0])
                if data_e.get(ip_dev) == None:
                    data_e[ip_dev] = []
                    data_e[ip_dev].append(out_val)
                else:
                    data_e[ip_dev].append(out_val)

    for dev, entries in data_e.items():
        for entry in data_e[dev]:
           #log.append("{} : {}".format(dev, entry))
           log.append("{}".format(entry))
    with open(filename, 'w') as f:
        f.writelines(log)
    return data_e


if __name__ == '__main__':
    with open('devices0.yaml') as f:
        devices = yaml.safe_load(f)
        #send_commands_to_devices(devices, "commands_result.log", 4, show = commands)
        send_commands_to_devices(devices, "commands_result.log", 4, config = commands_config)
