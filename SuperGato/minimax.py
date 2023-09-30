import math
import random
from copy import deepcopy


def es_nodo_terminal(tablero):
    """
    Revisa si el juego ha terminado dado un tablero. Devuelve True o False
    Hay dos opciones que devuelven 'True':
    1) 'X' o 'O' ganó
    2) No hay más posiciones válidas para jugar.
    """
    return tablero.revisar_ganador() != 0 or tablero.jugadas_disponibles() == []


def fichaOponente(ficha):
    if ficha == "O":
        return "X"
    else:
        return "O"


def minimax(tablero, profundidad, alpha, beta, funcion_puntaje, maximizar, ficha):
    """
    Algotimo Minimax. Dado el estado actual del juego, alpha, beta,
    y la función de puntuación devuelve (posición, puntaje):

    1) posicion = donde jugar
    2) puntaje = puntuación
    """

    # Primero revisamos si estamos en el nodo terminal (o el juego ha terminado en la profundidad actual)
    es_terminal = es_nodo_terminal(tablero)
    ficha_oponente = fichaOponente(ficha)
    if profundidad == 0 or es_terminal:
        if es_terminal:
            if tablero.revisar_ganador() == ficha:  # Ganó el computador
                return (None, math.inf)

            elif tablero.revisar_ganador() == ficha_oponente:  # Ganó el "Humano"
                return (None, -math.inf)

            else:  # La partida se terminó, no hay más moivmientos válidos
                return (None, 0)

        else:  # Profundidad es 0
            if maximizar:
                return (None, funcion_puntaje(tablero, ficha))
            else:
                return (None, -funcion_puntaje(tablero, ficha_oponente))

    if maximizar:  # Turno del computador en la profundidad actual
        # TODO: Obtener jugadas disponibles [HINT: Usa el método jugadas_disponibles()]
        posiciones_validas = None # CAMBIAR

        # Iniciamos un puntaje muy bajo
        puntaje = -math.inf

        # Elegir un movimiento random si no hay uno mejor
        posicion = random.choice(posiciones_validas)

        # Expandimos los nodos para cada columna válida
        for jugada in posiciones_validas:
            # TODO: Crear una copia del tablero [HINT: Usa deepcopy]

            # TODO: Ejecutar la jugada en la copia del tablero

            # TODO: Llamado recursivo de minimax

            # TODO: Revisamos si la nueva jugada es mejor y actualizamos puntaje y posicion

            pass

        return posicion, puntaje

    else:  # Turno del "Humano" en la profundidad actual
        # TODO: Obtener jugadas disponibles [HINT: Usa el método jugadas_disponibles()]
        posiciones_validas = None # CAMBIAR

        # Iniciamos un puntaje muy alto
        puntaje = math.inf

        # Movimiento random si no hay uno mejor
        posicion = random.choice(posiciones_validas)

        # Expandimos los nodos para cada columna válida
        for jugada in posiciones_validas:
            # TODO: Crear una copia del tablero [HINT: Usa deepcopy]

            # TODO: Ejecutar la jugada en la copia del tablero

            # TODO: Llamado recursivo de minimax

            # TODO: Revisamos si la nueva jugada es mejor y actualizamos puntaje y posicion

            pass

        return posicion, puntaje
