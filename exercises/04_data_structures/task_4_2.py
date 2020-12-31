# -*- coding: utf-8 -*-
"""
Задание 4.2

Преобразовать строку mac из формата XXXX:XXXX:XXXX в формат XXXX.XXXX.XXXX

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

mac = "AAAA:BBBB:CCCC"
m0 = mac.replace(":", ".")
print(m0)
#Out[172]: 'AAAA.BBBB.CCCC'
