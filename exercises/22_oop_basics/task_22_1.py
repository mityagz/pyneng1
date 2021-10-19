# -*- coding: utf-8 -*-

"""
Задание 22.1

Создать класс Topology, который представляет топологию сети.

При создании экземпляра класса, как аргумент передается словарь, который описывает топологию.
Словарь может содержать дублирующиеся соединения.

Дублем считается ситуация, когда в словаре есть такие пары:
    ('R1', 'Eth0/0'): ('SW1', 'Eth0/1') и ('SW1', 'Eth0/1'): ('R1', 'Eth0/0')

В каждом экземпляре должна быть создана переменная topology, в которой содержится словарь топологии, но уже без дублей.

Пример создания экземпляра класса:
In [2]: top = Topology(topology_example)

После этого, должна быть доступна переменная topology:

In [3]: top.topology
Out[3]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}


"""

topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}

class Topology:
    def __init__(self, topo):
        t = {}
        for i in topo.keys():
        # it's the first variant
        #    if i != t.get(topo[i]):
        #        t[i] = topo[i]
        # it's the second variant
            if i == topo.get(topo.get(i)):
                if t.get(i) == None and t.get(topo.get(i)) == None:
                    t[i] = topo[i]
            else:
                t[i] = topo[i]
        self.topology = t

    def gettopo(self):
        return self.topology

def main():
    top = Topology(topology_example)
    for t in (top.gettopo()):
        print(t, (top.gettopo())[t])

if __name__ == "__main__":
    main()
