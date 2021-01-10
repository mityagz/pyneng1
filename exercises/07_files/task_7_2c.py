# -*- coding: utf-8 -*-
"""
Задание 7.2c

Переделать скрипт из задания 7.2b:
* передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

Внутри, скрипт должен отфильтровать те строки, в исходном файле конфигурации,
в которых содержатся слова из списка ignore.
И записать остальные строки в итоговый файл.

Проверить работу скрипта на примере файла config_sw1.txt.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

ignore = ["duplex", "alias", "Current configuration"]

import sys

out_list = []

with open(sys.argv[1], 'r') as f:
  with open(sys.argv[2], 'w') as fo:
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

