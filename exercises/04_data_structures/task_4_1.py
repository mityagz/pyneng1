# -*- coding: utf-8 -*-
"""
Задание 4.1

Используя подготовленную строку nat, получить новую строку, в которой
в имени интерфейса вместо FastEthernet написано GigabitEthernet.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

nat = "ip nat inside source list ACL interface FastEthernet0/1 overload"

s0 = nat.replace("Fast","Gigabit")
print(s0)
#Out[170]: 'ip nat inside source list ACL interface GigabitEthernet0/1 overload'
