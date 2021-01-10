# -*- coding: utf-8 -*-
"""
Задание 7.2b

Дополнить скрипт из задания 7.2a:
* вместо вывода на стандартный поток вывода,
  скрипт должен записать полученные строки в файл config_sw1_cleared.txt

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore.
Строки, которые начинаются на '!' отфильтровывать не нужно.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "Current configuration"]

import sys

out_list = []

with open(sys.argv[1], 'r') as f:
  with open('config_sw1_cleared.txt', 'w') as fo:
    for l in f:
        ar = l.strip()
        for w in ignore:
            if ar.startswith(w):
                break
        else:
            out_list.append(ar)
    # It is the first variant, writes list
    #fo.write('\n'.join(out_list))
            # the second variant write by string + '\n'
            #fo.write(ar +  '\n')
            # the third variant with writelines()
            #fo.writelines(ar + '\n')
    # the four variant
    out_list2 = []
    for x in out_list:
        out_list2.append(x + '\n')
    fo.writelines(out_list2)

