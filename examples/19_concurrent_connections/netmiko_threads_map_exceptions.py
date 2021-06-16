from concurrent.futures import ThreadPoolExecutor
from pprint import pprint
from datetime import datetime
import time
from itertools import repeat
import logging

import yaml
from netmiko import ConnectHandler, NetMikoAuthenticationException


logging.getLogger('paramiko').setLevel(logging.WARNING)

logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)


def send_show(device_dict, command):
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received:   {}'
    device_dict.pop('command', None)
    ip = device_dict['ip']
    logging.info(start_msg.format(datetime.now().time(), ip))
    if ip == '192.168.100.1': time.sleep(5)

    try:
        with ConnectHandler(**device_dict) as ssh:
            ssh.enable()
            result = ssh.send_command(command)
            logging.info(received_msg.format(datetime.now().time(), ip))
        return result
    except NetMikoAuthenticationException as err:
        logging.warning(err)


def send_command_to_devices(devices, command):
    data = {}
    with ThreadPoolExecutor(max_workers=2) as executor:
        #result = executor.map(send_show, devices, repeat(command))
        pprint([ dev['command'] for dev in devices ])
        result = executor.map(send_show, devices, [ dev['command'] for dev in devices ])
        for device, output in zip(devices, result):
            data[device['ip']] = output
    return data


if __name__ == '__main__':
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    #pprint(send_command_to_devices(devices, 'sh ip int br'))
    #pprint(send_command_to_devices(devices[0:len(devices) - 1], 'show system uptime'))
    #pprint(send_command_to_devices(devices[0:len(devices)], devices[len(devices)-1]['command']))
    pprint(send_command_to_devices(devices[0:len(devices)], devices))

