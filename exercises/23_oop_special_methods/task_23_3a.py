# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
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

topology_example2 = {
    ("R1", "Eth0/4"): ("R7", "Eth0/0"),
    ("R1", "Eth0/6"): ("R9", "Eth0/0"),
}


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)
        self.t0 = topology_dict

    def __iter__(self):
        return iter([ (k, v) for k, v in self.topology.items() ])
    
    def _normalize(self, topo):
        t = {}
        for i in topo.keys():
            if i == topo.get(topo.get(i)):
                if t.get(i) == None and t.get(topo.get(i)) == None:
                    t[i] = topo[i]
            else:
                    t[i] = topo[i]
        return t
    
    def _get_topo(self):
        return self.t0

    def __add__(self, tp1):
        t2 = self.t0.copy()
        t1 = tp1._get_topo()
        for k in t1:
            t2[k] = t1[k]
        return Topology(t2)


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
    t1 = Topology(topology_example)
    t2 = Topology(topology_example2)
    t3 = t1 + t2
    print(t3.gettopo())
    top = Topology(topology_example)
    for link in top:
        pass

    """
    top.delete_link(("SW1", "Eth0/2"), ("R2", "Eth0/0"))
    for t in (top.gettopo()):
        print(t, (top.gettopo())[t])
    print("-----------------")
    top.delete_node('SW1')
    top.delete_node('R4')
    print(top.gettopo())
    """
if __name__ == "__main__":
   main()
