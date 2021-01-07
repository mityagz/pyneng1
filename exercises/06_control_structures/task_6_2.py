# -*- coding: utf-8 -*-
"""
Задание 6.2

1. Запросить у пользователя ввод IP-адреса в формате 10.0.1.1
2. В зависимости от типа адреса (описаны ниже), вывести на стандартный поток вывода:
   'unicast' - если первый байт в диапазоне 1-223
   'multicast' - если первый байт в диапазоне 224-239
   'local broadcast' - если IP-адрес равен 255.255.255.255
   'unassigned' - если IP-адрес равен 0.0.0.0
   'unused' - во всех остальных случаях


Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

i = 0
oct = []
ip = input('Введите ip адрес:')
correct_ip = False

f_digit = f_dot_delim = f_range = True

while not correct_ip:
    oct = ip.split('.')
    if len(oct) !=  4:
        print('Len isn\'t OK')
        f_dot_delim = False
    for d in oct:
        i += 1
        if not d.isdigit():
            f_digit = False
            print('oct {} contains not digit'.format(i))
            break
        else:
            if int(d) < 0 or int(d) > 255:
                f_range = False
                print('oct {} out of range'.format(i))
                break
    if not f_digit or not f_dot_delim or not f_range:
        ip = input('Введите ip адрес:')
        f_digit = f_dot_delim = f_range = True
        i = 0
    else:
        correct_ip = True
        break

if int(oct[0]) >= 1 and int(oct[0]) <= 223:
    print('unicast')
elif int(oct[0]) >= 224 and int(oct[0]) <= 239:
    print('multicast')
elif int(oct[0]) == 255 and int(oct[1]) == 255 and int(oct[2]) == 255 and int(oct[3]) == 255:
    print('local broadcast')
elif int(oct[0]) == 0 and int(oct[1]) == 0 and int(oct[2]) == 0 and int(oct[3]) == 0:
    print('unassigned')
else:
    print('unused')
