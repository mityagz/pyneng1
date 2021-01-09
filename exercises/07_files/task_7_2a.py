# -*- coding: utf-8 -*-
"""
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт:
  Скрипт не должен выводить команды, в которых содержатся слова,
  которые указаны в списке ignore.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "Current configuration"]

import sys


with open(sys.argv[1], 'r') as f:
    for l in f:
        fl = 0
        ar = l.strip()
        if ar.startswith('!'):
            fl = 1
        else:
            for w in ignore:
                if ar.startswith(w):
                    fl = 1
        if not fl:
                print(ar)


with open(sys.argv[1], 'r') as f:
 for l in f:
    ar = l.strip()
    if not ar.startswith('!') and not ar.startswith(ignore[2]):
        if ar.split(' ')[0] in ignore:
            pass
        else:
            print(ar)


with open(sys.argv[1], 'r') as f:
 for l in f:
    ar = l.strip()
    if ar.startswith('!') or ar.split(' ')[0] in ignore:
            pass
    else:
            print(ar)

with open(sys.argv[1], 'r') as f:
 for l in f:
    ar = l.strip()
    for w in ignore:
        if ar.startswith(w) or ar.startswith('!'):
            break
    else:
            print(ar)

ignore.append('!')

with open(sys.argv[1], 'r') as f:
 for l in f:
    ar = l.strip()
    for w in ignore:
        if ar.startswith(w):
            break
    else:
            print(ar)
