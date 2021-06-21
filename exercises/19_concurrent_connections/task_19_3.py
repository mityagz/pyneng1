# -*- coding: utf-8 -*-
"""
Задание 19.3

Создать функцию send_command_to_devices, которая отправляет
разные команды show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять какую команду. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh int desc
Interface                      Status         Protocol Description
Et0/0                          up             up
Et0/1                          up             up
Et0/2                          admin down     down
Et0/3                          admin down     down
Lo9                            up             up
Lo19                           up             up
R3#sh run | s ^router ospf
router ospf 1
 network 0.0.0.0 255.255.255.255 area 0


Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
"""

# Этот словарь нужен только для проверки работа кода, в нем можно менять IP-адреса
# тест берет адреса из файла devices.yaml
commands = {
    "10.240.0.65": "show configuration protocols ospf",
    "10.240.0.66": "show interfaces brief",
    "10.248.0.65": "show interfaces descriptions",
    "10.248.0.66": "show interfaces descriptions",
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
    log = []
    futures_ssh = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_ssh = [ executor.submit(send_show, device, commands[device['ip']]) for device in devices ]
        for f in as_completed(future_ssh):
            try:
                result = f.result()
            except NetMikoAuthenticationException as e:
                print(e)
            else:
                data.update(result)
    
    for dev, entry in data.items():
        log.append("{} : {}".format(dev, entry))
    with open(filename, 'w') as f:
        f.writelines(log)
    return data


if __name__ == '__main__':
    with open('devices0.yaml') as f:
        devices = yaml.safe_load(f)
    pprint(send_command_to_devices(devices, commands, "commands_result.log", 4))
