# -*- coding: utf-8 -*-
"""
Задание 17.2

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает как аргумент вывод команды sh version одной строкой (не имя файла)
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

У функции write_inventory_to_csv должно быть два параметра:
 * data_filenames - ожидает как аргумент список имен файлов с выводом sh version
 * csv_filename - ожидает как аргумент имя файла (например, routers_inventory.csv), в который будет записана информация в формате CSV
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает


Функция write_inventory_to_csv должна делать следующее:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в CSV файл

В файле routers_inventory.csv должны быть такие столбцы:
* hostname, ios, image, uptime

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается на sh_vers.
Вы можете раскомментировать строку print(sh_version_files), чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
"""

import glob
import re
import csv

sh_version_files = glob.glob("sh_vers*")
# print(sh_version_files)

headers = ["hostname", "ios", "image", "uptime"]

def parse_sh_version0(sh_ver):
    m = re.search(r'Cisco IOS Software.*Version (?P<ver>\S+), RELEASE SOFTW', sh_ver)
    m1 = re.search(r'router uptime is (?P<uptime>.*)\n', sh_ver)
    m2 =  re.search(r'System image file is (?P<image>.*)', sh_ver)
    if m and m1 and m2:
        return("{}".format(m.group('ver')), "{}".format(m2.group('image')), m1.group('uptime'))

def parse_sh_versioni1(sh_ver):
    #m = re.search(r'^Cisco IOS Software, .*, Version (?P<ver>\S+), RELEASE SOFTW.*\n'
    #              r'.*router uptime is (?P<uptime>.*)\n.*\n'
    #              r'.*System image file is \"(?P<image>.*)\"\n.*', sh_ver, re.DOTALL)
    m = re.search(r'Cisco IOS Software, .*, Version (?P<ver>\S+), RELEASE SOFTW.*\n.*'
                  r'.*router uptime is (?P<uptime>.*)\n.*\n'
                  r'.*System image file is \"(?P<image>.*)\"\n.*', sh_ver, re.DOTALL)
    if m:
        print("{}".format(m.group('ver')), "{}".format(m.group('image')), m.group('uptime'))
        return("{}".format(m.group('ver')), "{}".format(m.group('image')), m.group('uptime'))

def parse_sh_version2(sh_ver):
    parsed = {}
    for l in sh_ver.split('\n'):
        m = re.search(r'Cisco IOS Software, .*, Version (?P<ver>\S+), RELEASE SOFTW'
                      r'|System image file is \"(?P<image>.*)\"'
                      r'|router uptime is (?P<uptime>.*)', l)
        if m:
            parsed[m.lastgroup] = m.group(m.lastgroup)
    return("{}".format(parsed['ver']), "{}".format(parsed['image']), parsed['uptime'])

def parse_sh_version(sh_ver):
    m = re.search(r'^Cisco IOS Software, (\S|\w|\d|\s)*?, Version (?P<ver>\S+)?, RELEASE SOFTW.*'
                  r'router uptime is (?P<uptime>.*)\n.*\n'
                  r'System image file is \"(?P<image>.*)\"\n.*', sh_ver, re.DOTALL)
    if m:
        return("{}".format(m.group('ver')), "{}".format(m.group('image')), m.group('uptime'))

def write_inventory_to_csv(data_filenames, csv_filename):
    res = []
    for filename in data_filenames:
        matchhost = re.search(r'.*_(?P<host>\S+).txt', filename)
        if matchhost:
            host = matchhost.group('host')
            with open(filename, 'r') as f:
                r = list(parse_sh_version(f.read()))
                r.insert(0, host)
                res.append(r)
    res.insert(0, headers)

    with open(csv_filename, 'w') as f:
        writer = csv.writer(f)
        for row in res:
            writer.writerow(row)

if __name__ == '__main__':
    write_inventory_to_csv(sh_version_files, 'routers_inventory.csv')
