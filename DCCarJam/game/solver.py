from copy import deepcopy
from binary_heap import BinaryHeap
from node import Node
import time


class Solver(object):
    """Implementación de A*

        Atributos:
        board: Configuración inicial del puzzle
        h: Heurística
    """

    def __init__(self, initial_state, heuristic, weight=1):
        self.expansions = 0
        self.generated = 0
        self.initial_state = initial_state
        self.weight = weight
        initial_state.set_heuristic(heuristic)

    def search(self):
        self.start_time = time.process_time()
        self.open = BinaryHeap()
        self.expansions = 0
        w = self.weight
        initial_node = Node(self.initial_state)
        initial_node.g = 0
        initial_node.h = self.initial_state.heuristic()
        initial_node.key = 1000*1*initial_node.h  # Asignamos el valor f
        self.open.insert(initial_node)
        # Para cada estado alguna vez generado, generated almacena el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state.id()] = initial_node

        while not self.open.is_empty():
            n = self.open.extract()  # Extrae n de la open

            if n.state.is_goal():
                self.end_time = time.process_time()
                return n

            succ = n.state.successors()
            self.expansions += 1

            for action, child_state, cost in succ:
                child_node = self.generated.get(child_state.id())
                is_new = child_node is None
                path_cost = n.g + cost  # Costo del camino encontrado hasta child_state
                if is_new or path_cost < child_node.g:
                    """si vemos este estado por primera vez o lo vemos por
                       un mejor camino, entonces lo agregamos a open"""
                    if is_new:  # Creamos el nodo si no existe
                        child_node = Node(child_state, n)
                        child_node.h = child_state.heuristic()
                        self.generated[child_state.id()] = child_node
                    else:  # Actualizamos el padre si existe
                        child_node.parent = n

                    child_node.action = action
                    child_node.g = path_cost
                    child_node.key = child_node.g + w * child_node.h  # Actualizamos el f del child_node
                    self.open.insert(child_node)  # Inserta child_node a la open si no estaba
        self.end_time = time.process_time()       # o actualiza su prioridad si ya estaba
        return None

    def solution(self, board, moves):
        output = ''
        output += "; ".join(["{} {}".format(move[0], move[1]) for move in moves])
        cars = deepcopy(board.cars)
        for move in moves:
            car = [x for x in cars if x.name == move[0]][0]
            output += '\nMOVE {} {}\n'.format(move[0], move[1])
            car.move(move[1], 1)
            output += self.initial_state.prettify(cars)
        return output
