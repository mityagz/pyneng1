# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще нет в топологии
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение "Cоединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


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

    def add_link(self, a, b):
        if self.topology.get(a) == b or self.topology.get(b) == a:
            print('Такое соединение существует')
        elif (self.topology.get(a) != None or self.topology.get(b) != None):
            print('Cоединение с одним из портов существует')
        self.topology[a] = b

def main():
    top = Topology(topology_example)
    top.delete_link(("SW1", "Eth0/2"), ("R2", "Eth0/0"))
    for t in (top.gettopo()):
        print(t, (top.gettopo())[t])
    print("-----------------")
    top.delete_node('SW1')
    top.delete_node('R4')
    print(top.gettopo())
    top.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    print(top.gettopo())
    top.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    top.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))

if __name__ == "__main__":
   main()
