# -*- coding: utf-8 -*-
"""
Задание 6.2a
Сделать копию скрипта задания 6.2.
Добавить проверку введенного IP-адреса. Адрес считается корректно заданным, если он:
 - состоит из 4 чисел (а не букв или других символов)
 - числа разделенны точкой
 - каждое число в диапазоне от 0 до 255
Если адрес задан неправильно, выводить сообщение:
 'Неправильный IP-адрес'
 Сообщение должно выводиться только один раз.
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
