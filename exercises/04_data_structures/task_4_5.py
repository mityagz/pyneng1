# -*- coding: utf-8 -*-
"""
Задание 4.5

Из строк command1 и command2 получить список VLANов,
которые есть и в команде command1 и в команде command2 (пересечение).

Результатом должен быть такой список: ['1', '3', '8']

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

command1 = "switchport trunk allowed vlan 1,2,3,5,8"
command2 = "switchport trunk allowed vlan 1,3,8,9"

s0 = list(set([ int(v0) for v0 in command1.split(" ")[-1].split(",") if v0.isdigit() ]) & set([ int(v1) for v1 in command2.split(" ")[-1].split(",") if v1.isdigit() ]))
s0.sort()
print(s0)
