# -*- coding: utf-8 -*-
"""
Задание 19.3a

Создать функцию send_command_to_devices, которая отправляет
список указанных команды show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять какие команды. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом каждой команды надо написать имя хоста и саму команду):

R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          87   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R1#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.30.0.1               -   aabb.cc00.6530  ARPA   Ethernet0/3.300
Internet  10.100.0.1              -   aabb.cc00.6530  ARPA   Ethernet0/3.100
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down
R3#sh ip route | ex -

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
O        10.1.1.1/32 [110/11] via 192.168.100.1, 07:12:03, Ethernet0/0
O        10.30.0.0/24 [110/20] via 192.168.100.1, 07:12:03, Ethernet0/0


Порядок команд в файле может быть любым.

Для выполнения задания можно создавать любые дополнительные функции, а также использовать функции созданные в предыдущих заданиях.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
"""

# Этот словарь нужен только для проверки работа кода, в нем можно менять IP-адреса
# тест берет адреса из файла devices.yaml
commands = {
    "10.240.0.65": [ "show configuration protocols ospf", "show configuration protocols lldp" ],
    "10.240.0.66": [ "show interfaces brief", "show configuration protocols lldp" ],
    "10.248.0.65": [ "show interfaces descriptions" ],
    "10.248.0.66": [ "show interfaces descriptions", "show configuration protocols lldp" ],
}

from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
from datetime import datetime
import time
from itertools import repeat
import logging

import yaml
from netmiko import ConnectHandler

from paramiko.ssh_exception import AuthenticationException
#from netmiko.ssh_exception import NetmikoTimeoutException

logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)

start_msg = '===> {} Connection: {}'
received_msg = '<=== {} Received: {}'


def send_show(device_dict, command):
    ip = device_dict['ip']
    print(ip, command)
    logging.info(start_msg.format(datetime.now().time(), ip))
    with ConnectHandler(**device_dict) as ssh:
        prompt = ssh.find_prompt()
        ssh.write_channel(f"{command}\n")
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


def send_command_to_devices(devices, commands_dict, filename, limit=3):
    data = {}
    data_e = {}
    log = []
    futures_ssh = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        print([ "{} {}".format(device['ip'], c) for device in devices for c in commands[device['ip']]])
        futures_ssh = [ executor.submit(send_show, device, c) for device in devices for c in commands[device['ip']] ]
        for f in as_completed(futures_ssh):
            try:
                result = f.result()
            except NetMikoAuthenticationException as e:
                print(e)
            else:
                data.update(result)
                ip_dev = ((list(result.keys()))[0])
                out_val = ((list(result.values()))[0])
                if data_e.get(ip_dev) == None:
                    data_e[ip_dev] = []
                    data_e[ip_dev].append(out_val)
                else:
                    data_e[ip_dev].append(out_val)

    for dev, entries in data_e.items():
        for entry in data_e[dev]:
            log.append("{} : {}".format(dev, entry))
    with open(filename, 'w') as f:
        f.writelines(log)
    return data


if __name__ == '__main__':
    with open('devices0.yaml') as f:
        devices = yaml.safe_load(f)
    #pprint(send_command_to_devices(devices, commands, "commands_result.log", 4))
    send_command_to_devices(devices, commands, "commands_result.log", 4)
