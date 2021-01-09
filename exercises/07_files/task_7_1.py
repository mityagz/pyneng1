# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком виде:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

out_f = "Prefix {:25}\nAD/Metric {:25}\nNext-Hop {:25}\nLast update {:25}\nOutbound Interface {:25}\n"

with open("exercises/07_files/ospf.txt", 'r') as ospf_f:
    for l in ospf_f:
        al = ((l.strip().replace(',', '').replace('[', '').replace(']', '').split()))
        print(out_f.format(al[1], al[2], al[4], al[5], al[6]))
