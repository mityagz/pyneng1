# -*- coding: utf-8 -*-
"""
Задание 17.1

Создать функцию write_dhcp_snooping_to_csv, которая обрабатывает
вывод команды show dhcp snooping binding из разных файлов и записывает обработанные данные в csv файл.

Аргументы функции:
* filenames - список с именами файлов с выводом show dhcp snooping binding
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Например, если как аргумент был передан список с одним файлом sw3_dhcp_snooping.txt:
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:E9:BC:3F:A6:50   100.1.1.6        76260       dhcp-snooping   3    FastEthernet0/20
00:E9:22:11:A6:50   100.1.1.7        76260       dhcp-snooping   3    FastEthernet0/21
Total number of bindings: 2

В итоговом csv файле должно быть такое содержимое:
switch,mac,ip,vlan,interface
sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21


Проверить работу функции на содержимом файлов sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt.
Первый столбец в csv файле имя коммутатора надо получить из имени файла, остальные - из содержимого в файлах.

"""

import re
import csv

def write_dhcp_snooping_to_csv(filenames, output):
    res = []
    for f in filenames:
        hostname = f.split('_')[0]
        with open(f, 'r') as ff:
            for line in ff:
                match = re.search(r'(?P<mac>(((\d|\w){2}:){5})(\d|\w){2})\s+'
                                  r'(?P<ip>((\d{1,3})\.){3}(\d{1,3}))\s+'
                                  r'\d+\s+dhcp-snooping\s+(?P<vid>\d+)\s+'
                                  r'(?P<intf>\S+)', line)
                if(match):
                    r = list(match.group('mac', 'ip', 'vid', 'intf'))
                    r.insert(0, hostname)
                    res.append(r)

    res.insert(0, [ 'switch' , 'mac', 'ip', 'vlan', 'interface' ])
    print(res)
    with open(output, 'w') as fout:
       writer = csv.writer(fout)
       for row in res:
            writer.writerow(row)

if __name__ == '__main__':
    write_dhcp_snooping_to_csv([ 'sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt' ], 'dhcp.csv')
