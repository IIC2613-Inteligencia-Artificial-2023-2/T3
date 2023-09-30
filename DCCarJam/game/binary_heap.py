# Implementacion de un Heap binario en donde cada elemento del heap
# tiene la propiedad heap_index que corresponde a su posicion en el heap
from copy import deepcopy


class BinaryHeap:
    def __init__(self, max_size=10000000):
        self.array = [None]*(max_size+1)
        self.size = 0

    def clear(self):  # clears the content of the heap
        self.size = 0

    def percolatedown(self, hole, element):
        if self.size == 0:
            return
        while 2*hole <= self.size:
            child = 2*hole
            if child != self.size and self.array[child+1].key < self.array[child].key:
                child += 1
            if self.array[child].key < element.key:
                self.array[hole] = self.array[child]
                self.array[hole].heap_index = hole
            else:
                break
            hole = child
        self.array[hole] = element
        element.heap_index = hole

    def percolateup(self, hole, element):
        if self.size == 0:
            return
        while hole > 1 and element.key < self.array[hole//2].key:
            self.array[hole] = self.array[hole//2]
            self.array[hole].heap_index = hole
            hole //= 2
        self.array[hole] = element
        element.heap_index = hole

    def percolateupordown(self, hole, element):
        if self.size == 0:
            return
        if hole > 1 and element.key < self.array[hole//2].key:
            self.percolateup(hole, element)
        else:
            self.percolatedown(hole, element)

    def top(self):
        if self.size == 0:
            return None
        else:
            return self.array[1]

    def extract(self):
        if self.size == 0:
            return None
        element = self.array[1]
        element.heap_index = 0
        self.percolatedown(1, self.array[self.size])
        self.size -= 1
        return element

    def insert(self, element):
        if element.heap_index == 0:  # element no esta en el heap
            self.size += 1
            self.percolateup(self.size, element)
        else:  # element esta en el heap; suponemos que su key ha cambiado
            self.percolateupordown(element.heap_index, element)

    def is_empty(self):
        return self.size == 0

    def reorder(self):
        # Para que el método tenga efecto se debe modificar la key de los nodos previamente
        for i in range(2, self.size+1):
            self.percolateup(i, self.array[i])

    def get_nodes(self):
        copy = deepcopy(self)
        node_list = []
        while not copy.is_empty():
            node_list.append(copy.extract())
        return node_list
