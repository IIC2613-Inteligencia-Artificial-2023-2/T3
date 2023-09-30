# -*- coding: utf-8 -*-
"""
This module defines the Board and Car classes for the rush-hour game

The Car class serve more to store car data and logic involving possible
moves of car in the board is defined in the Board class
"""
from copy import deepcopy
from collections import defaultdict


class Orientation(object):
    """Dirección del auto"""
    HORIZONTAL = 0
    VERTICAL = 1


class Car(object):
    """Clase de auto para el juego

    Atributos:
        name: character
        coord: Coordenada del auto en el tablero
        length: Largo del auto
        orientation: Alineamiento horizontal o vertical
        is_red_car: el auto por ser liberado

    """

    def __init__(self, name, coord, length, orientation, is_red_car=None):
        self.name = name
        self.coord = coord
        self.length = length - 1
        self.orientation = orientation
        self.is_red_car = is_red_car

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        if self.orientation == Orientation.HORIZONTAL:
            other_coord = {'x': self.coord['x'] + self.length,
                           'y': self.coord['y']}
            return "{} [{},{}]".format(self.name, self.coord, other_coord)
        else:
            other_coord = {'x': self.coord[
                'x'], 'y': self.coord['y'] + self.length}
            return "{} [{},{}]".format(self.name, self.coord, other_coord)

    def move(self, direction, distance):
        """Dada la dirección y distancia, mueve el auto"""
        if direction == 'up':
            self.coord['y'] -= distance

        if direction == 'down':
            self.coord['y'] += distance

        if direction == 'left':
            self.coord['x'] -= distance

        if direction == 'right':
            self.coord['x'] += distance

    @staticmethod
    def createFromBoardInfo(name, coords):
        def plane(coords):
            if coords[0]['x'] != coords[1]['x'] and coords[0]['y'] == coords[1]['y']:
                return Orientation.HORIZONTAL
            else:
                return Orientation.VERTICAL
        return Car(name, coords[0], len(coords), plane(coords), is_red_car=(name == 'r'))


class Board(object):
    """Clase del tablero para crear el tablero de juego

    Atributos:
        cars: Lista de autos en el tablero de juego
        size: Tamaño del tablero
    """

    def __init__(self, cars, width=6, height=6):
        self.size = {'x': height, 'y': width}
        self.cars = cars
        self.depth = 0
        self.hval = 0

    def __eq__(self, other):
        return self.cars == other.other

    def __str__(self):
        self.cars.sort(key=lambda x: x.name)
        return str(self.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())

    def id(self):
        """Retorna un id del tablero.
           Si 2 tableros tienen la misma configuración, entonces también tienen el mismo id"""
        return hash(str(self))

    def set_heuristic(self, heur="h0"):
        if heur == "h0":
            Board.heuristic = Board.h0
        elif heur == "h1":
            Board.heuristic = Board.h1
        elif heur == "h2":
            Board.heuristic = Board.h2

    def h0(self):
        """Zero Heuristic, Dijkstra's Algorithm"""
        return 0
    
    def h1(self):
        """Distancia del auto rojo a la salida"""
        red_car = [car for car in self.cars if car.is_red_car][0]
        return self.size['x'] - red_car.coord['x'] - red_car.length - 1

    def h2(self):
        """Cantidad de autos que bloquean al auto rojo"""
        red_car = [
            car for car in self.cars if car.is_red_car][0]
        if red_car.coord['x'] == 4:
            return 0
        blockingcars = 1
        for car in self.cars:
            if car.orientation == Orientation.VERTICAL and car.coord['x'] >= (red_car.coord['x'] + red_car.length) and (car.coord['y'] <= red_car.coord['y'] and car.coord['y'] + car.length > red_car.coord['y']):
                blockingcars += 1
        return blockingcars
    
    # TODO: Completar con tu propia heurística
    def h3(self):
        """Implementa tu propia heurística de trabajo"""
        return None

    @staticmethod
    def readFromfile(filename):
        """Lee un puzzle de un archivo y crea una instancia del tablero,
           identifica al auto rojo y las dimensiones del tablero"""
        def get_coord(row_idx):
            def result(col_idx, value):
                return (value, {'y': row_idx, 'x': col_idx})
            return result

        def flatten(l):
            return [item for sublist in l for item in sublist]

        puzzle_file = open(filename, 'r')
        raw_board = [list(line.strip()) for line in puzzle_file]
        coords_board = [map(get_coord(row_idx), [i for i in range(len(row))], row)
                        for row_idx, row in enumerate(raw_board)]

        cars_board = flatten([filter(lambda c: c[0].isalpha(), list(row))
                              for row in list(coords_board)])
        raw_cars = defaultdict(list)
        for (k, v) in cars_board:
            raw_cars[k].append(v)
        cars = []
        for i in raw_cars:
            cars.append(Car.createFromBoardInfo(i, raw_cars[i]))
        return Board(cars, len(raw_board), len(raw_board[0]))

    def successors(self):
        """Explora los estados de movidas posibles. También checkea si un auto choca con otro o con una pared"""
        board = self.game_board(self.cars)
        successors = []
        for car in self.cars:
            if car.orientation == Orientation.VERTICAL:
                # UP
                if car.coord['y'] - 1 >= 0 and board[car.coord['y'] - 1][car.coord['x']] == '.':
                    new_cars = deepcopy(self.cars)
                    new_car = [x for x in new_cars if x.name == car.name][0]
                    new_car.coord['y'] -= 1
                    successors.append([[car.name, 'up'], Board(new_cars, self.size["y"], self.size["x"]), 1])
                # DOWN
                if car.coord['y'] + car.length + 1 <= (self.size['x'] - 1) and board[car.coord['y'] + car.length + 1][car.coord['x']] == '.':
                    new_cars = deepcopy(self.cars)
                    new_car = [x for x in new_cars if x.name == car.name][0]
                    new_car.coord['y'] += 1
                    successors.append([[car.name, 'down'], Board(new_cars, self.size["y"], self.size["x"]), 1])
            else:
                # LEFT
                if car.coord['x'] - 1 >= 0 and board[car.coord['y']][car.coord['x'] - 1] == '.':
                    new_cars = deepcopy(self.cars)
                    new_car = [x for x in new_cars if x.name == car.name][0]
                    new_car.coord['x'] -= 1
                    successors.append([[car.name, 'left'], Board(new_cars, self.size["y"], self.size["x"]), 1])
                # RIGHT
                if car.coord['x'] + car.length + 1 <= (self.size['y'] - 1) and board[car.coord['y']][car.coord['x'] + car.length + 1] == '.':
                    new_cars = deepcopy(self.cars)
                    new_car = [x for x in new_cars if x.name == car.name][0]
                    new_car.coord['x'] += 1
                    successors.append([[car.name, 'right'], Board(new_cars, self.size["y"], self.size["x"]), 1])

        return successors

    def game_board(self, cars):
        """Dado un conjunto de autos, crea un array 2D del puzzle"""
        board = [['.' for col in range(self.size['x'])]
                 for row in range(self.size['y'])]
        for car in cars:
            if car.orientation == Orientation.HORIZONTAL:
                x_start = car.coord['x']
                x_stop = car.coord['x'] + car.length
                for x in range(x_start, x_stop + 1):
                    board[car.coord['y']][x] = car.name
            else:
                y_start = car.coord['y']
                y_stop = car.coord['y'] + car.length
                for y in range(y_start, y_stop + 1):
                    board[y][car.coord['x']] = car.name
        return board

    def prettify(self, cars):
        """Para hacer prints más bonitos"""
        board = self.game_board(cars)
        output = ''
        for line in board:
            output += "".join(line) + '\n'
        return output

    def is_goal(self):
        """Mira si el auto rojo puede salir"""
        red_car = [car for car in self.cars if car.is_red_car][0]
        return red_car.coord['x'] + red_car.length == self.size['x'] - 1
