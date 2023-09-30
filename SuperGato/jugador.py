import math
import numpy as np
from minimax import minimax
import random


class JugadorIA():
    def __init__(self, ficha, profundidad, funcion_puntaje):
        self.ficha = ficha
        self.profundidad = profundidad
        self.funcion_puntaje = funcion_puntaje

    def elegir_jugada(self, tablero):
        # Si el jugador es la IA
        # No usamos el valor acá, por lo que lo reemplazamos con _

        if tablero.jugada_anterior is None:
            posibles = tablero.jugadas_disponibles()
            return random.choice(posibles)

        posicion, _ = minimax(
            tablero=tablero,
            profundidad=self.profundidad,
            alpha=-math.inf,
            beta=math.inf,
            funcion_puntaje=self.funcion_puntaje,
            maximizar=True,
            ficha=self.ficha
        )

        return posicion


class JugadorRandom():
    def __init__(self, ficha):
        self.ficha = ficha

    def elegir_jugada(self, tablero):
        posibles = tablero.jugadas_disponibles()

        return random.choice(posibles)


class JugadorHumano():
    def __init__(self, ficha):
        self.ficha = ficha

    def elegir_jugada(self, tablero):
        # Si no hay jugadas disponibles, el juego termina
        if tablero.jugadas_disponibles() == []:
            return None

        # Si el jugador es humano
        # Pedimos la jugada al usuario
        print("Turno del jugador ", self.ficha)

        # Revisamos si existe una jugada anterior. Si existe estamos obligados a jugar en 
        # el subtablero que corresponde a la jugada anterior. Si este subtablero ya tiene
        # un ganador, podemos jugar en cualquier subtablero que no tenga ganador
        tablero_permitido = tablero.jugada_anterior
        if tablero_permitido is not None:
            if tablero[tablero_permitido[0:2]].ganador != 0:
                tablero_permitido = None
            elif tablero[tablero_permitido[0:2]].ganador == 0:
                tablero_permitido = tablero_permitido[0:2]

        if tablero_permitido is None:
            subtablero_x_elegido = False
            subtablero_y_elegido = False
            subtablero_correcto = False
            while not subtablero_correcto:
                while not subtablero_x_elegido:
                    tablero_x = input(
                        "Fila en donde está el subtablero a jugar (1, 2 o 3): ")
                    if not tablero_x.isnumeric() or int(tablero_x) not in range(1, 4):
                        print("Input inválido, vuelva a intentar")
                    else:
                        tablero_x = int(tablero_x) - 1
                        subtablero_x_elegido = True

                while not subtablero_y_elegido:
                    tablero_y = input(
                        "Columna en donde está el subtablero a jugar (1, 2 o 3): ")
                    if not tablero_y.isnumeric() or int(tablero_y) not in range(1, 4):
                        print("Input inválido, vuelva a intentar")
                    else:
                        tablero_y = int(tablero_y) - 1
                        subtablero_y_elegido = True

                if tablero[tablero_x, tablero_y].ganador != 0:
                    print("Subtablero con ganador, vuelva a intentar")
                    subtablero_x_elegido = False
                    subtablero_y_elegido = False
                
                else:
                    subtablero_correcto = True

        else:
            tablero_x = tablero_permitido[0]
            tablero_y = tablero_permitido[1]

        posicion_x_elegido = False
        posicion_y_elegido = False
        posicion_correcta = False
        while not posicion_correcta:
            while not posicion_x_elegido:
                print("Subtablero a jugar: ", tablero_x + 1, tablero_y + 1)
                posicion_x = input("Fila del subtablero a jugar (1, 2 o 3): ")
                if not posicion_x.isnumeric() or int(posicion_x) not in range(1, 4):
                    print("Input inválido, vuelva a intentar")
                else:
                    posicion_x = int(posicion_x) - 1
                    posicion_x_elegido = True

            while not posicion_y_elegido:
                posicion_y = input(
                    "Columna del subtablero a jugar (1, 2 o 3): ")
                if not posicion_y.isnumeric() or int(posicion_y) not in range(1, 4):
                    print("Input inválido, vuelva a intentar")
                else:
                    posicion_y = int(posicion_y) - 1
                    posicion_y_elegido = True

            if tablero[tablero_x, tablero_y].tablero[posicion_x][posicion_y] != 0:
                print("Posición ocupada, vuelva a intentar")
                posicion_x_elegido = False
                posicion_y_elegido = False
            else:
                posicion_correcta = True

        return np.array([tablero_x, tablero_y, posicion_x, posicion_y])
