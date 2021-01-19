# -*- coding: utf-8 -*-
"""
Задание 9.2a

Сделать копию функции generate_trunk_config из задания 9.2

Изменить функцию таким образом, чтобы она возвращала не список команд, а словарь:
    - ключи: имена интерфейсов, вида 'FastEthernet0/1'
    - значения: список команд, который надо выполнить на этом интерфейсе

Проверить работу функции на примере словаря trunk_config и шаблона trunk_mode_template.

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

def generate_trunk_config(intf_vlan_mapping, trunk_template):
    """
    {'FastEthernet0/1': [10, 20],
     'FastEthernet0/2': [11, 30],
     'FastEthernet0/4': [17]}
    trunk_template - список команд для порта в режиме access

    Возвращает список всех портов в режиме trunk с конфигурацией на основе шаблона
    """
    r = {}
    for intf, vids in intf_vlan_mapping.items():
        i = intf
        r[i] = []
        for t in trunk_template:
            if t.startswith('switchport trunk allowed vlan'):
                r[i].append(t + ' {}'.format(','.join([ str(v) for v in vids ])))
            else:
                r[i].append(t)
    return(r)

print(generate_trunk_config(trunk_config, trunk_mode_template))
print()
#print(generate_trunk_config(trunk_config_2, trunk_mode_template))
