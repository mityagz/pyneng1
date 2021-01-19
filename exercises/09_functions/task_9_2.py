# -*- coding: utf-8 -*-
"""
Задание 9.2

Создать функцию generate_trunk_config, которая генерирует конфигурацию для trunk-портов.

У функции должны быть такие параметры:

- intf_vlan_mapping: ожидает как аргумент словарь с соответствием интерфейс-VLANы такого вида:
    {'FastEthernet0/1': [10, 20],
     'FastEthernet0/2': [11, 30],
     'FastEthernet0/4': [17]}
- trunk_template: ожидает как аргумент шаблон конфигурации trunk-портов в виде списка команд (список trunk_mode_template)

Функция должна возвращать список команд с конфигурацией
на основе указанных портов и шаблона trunk_mode_template.
В конце строк в списке не должно быть символа перевода строки.

Проверить работу функции на примере словаря trunk_config и списка команд trunk_mode_template.
Если предыдущая проверка прошла успешно, проверить работу функции еще раз на словаре trunk_config_2
и убедится, что в итоговом списке правильные номера интерфейсов и вланов.


Пример итогового списка (перевод строки после каждого элемента сделан для удобства чтения):
[
'interface FastEthernet0/1',
'switchport mode trunk',
'switchport trunk native vlan 999',
'switchport trunk allowed vlan 10,20,30',
'interface FastEthernet0/2',
'switchport mode trunk',
'switchport trunk native vlan 999',
'switchport trunk allowed vlan 11,30',
...]


Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

trunk_mode_template = [
    "switchport mode trunk",
    "switchport trunk native vlan 999",
    "switchport trunk allowed vlan",
]

trunk_config = {
    "FastEthernet0/1": [10, 20, 30],
    "FastEthernet0/2": [11, 30],
    "FastEthernet0/4": [17],
}

trunk_config_2 = {
    "FastEthernet0/11": [120, 131],
    "FastEthernet0/15": [111, 130],
    "FastEthernet0/14": [117],
}


def generate_trunk_config(intf_vlan_mapping, trunk_template):
    """
    {'FastEthernet0/1': [10, 20],
     'FastEthernet0/2': [11, 30],
     'FastEthernet0/4': [17]}
    trunk_template - список команд для порта в режиме access

    Возвращает список всех портов в режиме trunk с конфигурацией на основе шаблона
    """
    r = []
    for intf, vids in intf_vlan_mapping.items():
        r.append('interface ' + intf)
        for t in trunk_template:
            if t.startswith('switchport trunk allowed vlan'):
                r.append(t + ' {}'.format(','.join([ str(v) for v in vids ])))
            else:
                r.append(t)
    return(r)

print(generate_trunk_config(trunk_config, trunk_mode_template))
print()
print(generate_trunk_config(trunk_config_2, trunk_mode_template))
