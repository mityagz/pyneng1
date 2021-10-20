# -*- coding: utf-8 -*-

"""
Задание 22.1c

Изменить класс Topology из задания 22.1b.

Добавить метод delete_node, который удаляет все соединения с указаным устройством.

Если такого устройства нет, выводится сообщение "Такого устройства нет".

Создание топологии
In [1]: t = Topology(topology_example)

In [2]: t.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление устройства:
In [3]: t.delete_node('SW1')

In [4]: t.topology
Out[4]:
{('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Если такого устройства нет, выводится сообщение:
In [5]: t.delete_node('SW1')
Такого устройства нет

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
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)
    
    def _normalize(self, topo):
        t = {}
        for i in topo.keys():
            if i == topo.get(topo.get(i)):
                if t.get(i) == None and t.get(topo.get(i)) == None:
                    t[i] = topo[i]
            else:
                    t[i] = topo[i]
        return t

    def gettopo(self):
        return self.topology

    def delete_link(self, a, b):
        if self.topology.get(a) == b:
            self.topology.pop(a)
            return
        if self.topology.get(b) == a:
            self.topology.pop(b)
            return
        print("Такого соединения нет")

    def delete_node(self, n):
        list_to_del = []
        for x, y in self.topology.items():
            ha = x[0]
            hb = y[0]
            if ha == n:
                list_to_del.append(x)
            if hb == n:
                list_to_del.append(x)
        #print(list_to_del)
        if len(list_to_del) == 0:
            print('Такого устройства нет')
            return
        else:
            for x in (list_to_del):
                self.topology.pop(x)

def main():
    top = Topology(topology_example)
    top.delete_link(("SW1", "Eth0/2"), ("R2", "Eth0/0"))
    for t in (top.gettopo()):
        print(t, (top.gettopo())[t])
    print("-----------------")
    top.delete_node('SW1')
    top.delete_node('R4')
    print(top.gettopo())

if __name__ == "__main__":
   main()
