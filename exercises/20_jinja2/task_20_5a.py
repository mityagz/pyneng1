# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует шаблоны из задания 20.5 для настройки VPN на маршрутизаторах на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству
* dst_device_params - словарь с параметрами подключения к устройству
* src_template - имя файла с шаблоном, который создает конфигурацию для одной строны туннеля
* dst_template - имя файла с шаблоном, который создает конфигурацию для второй строны туннеля
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов и данных на каждом устройстве с помощью netmiko.
Функция возвращает вывод с набором команд с двух марушртизаторов (вывод, которые возвращает метод netmiko send_config_set).

При этом, в словаре data не указан номер интерфейса Tunnel, который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel, взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 9.
И надо будет настроить интерфейс Tunnel 9.

Для этого задания нет теста!
"""

data = {
    "tun_num": None,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}

import yaml
from jinja2 import Environment, FileSystemLoader
import os
from task_20_1 import generate_config
from task_20_5 import create_vpn_config

def get_first_free_id_of_tun(dev1, dev2):
    return 0

def conf_vpn(dev, conf):
    return conf

def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    vpn_data_dict['tun_num'] = get_first_free_id_of_tun(src_device_params, dst_device_params)
    (c1, c2) = create_vpn_config(src_template, dst_template, data)
    res_conf1 = conf_vpn(src_device_params, c1)
    res_conf2 = conf_vpn(dst_device_params, c2)
    res_conf = res_conf1 + "\n\n\n" + res_conf2
    return res_conf


# так должен выглядеть вызов функции
if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    template_file1 = "templates/gre_ipsec_vpn_1.txt"
    template_file2 = "templates/gre_ipsec_vpn_2.txt"
    print(configure_vpn(devices[0], devices[1], template_file1, template_file2, data))
crypto isakmp policy {{ tun_num }}
 encr aes
 authentication pre-share
 group 5
 hash sha

"""
crypto isakmp key cisco address {{ wan_ip_2 }}

crypto ipsec transform-set AESSHA esp-aes esp-sha-hmac
 mode transport

crypto ipsec profile GRE
 set transform-set AESSHA

interface Tunnel {{ tun_num }}
 ip address {{ tun_ip_1}}
 tunnel source {{ wan_ip_1 }}
 tunnel destination {{ wan_ip_2 }}
 tunnel protection ipsec profile GRE
crypto isakmp policy {{ tun_num }}
 encr aes
 authentication pre-share
 group 5
 hash sha

crypto isakmp key cisco address {{ wan_ip_1}}

crypto ipsec transform-set AESSHA esp-aes esp-sha-hmac
 mode transport

crypto ipsec profile GRE
 set transform-set AESSHA

interface Tunnel {{ tun_num }}
 ip address {{ tun_ip_2}}
 tunnel source {{ wan_ip_2 }}
 tunnel destination {{ wan_ip_1 }}
 tunnel protection ipsec profile GRE
 """
