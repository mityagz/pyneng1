# -*- coding: utf-8 -*-
"""
Задание 4.6

Обработать строку ospf_route и вывести информацию на стандартный поток вывода в виде:
Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ospf_route = "      10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0"

l0 = ospf_route.replace(",", "").split()
print("Prefix{:>35}\nAD/Metric{:>35}\nNext-Hop{:>25}\nLast update{:>25}\nOutbound Interface{:>25}".format(l0[0], l0[1], l0[3], l0[4], l0[5]))