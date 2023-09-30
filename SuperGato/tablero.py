import numpy as np


FICHA = {
    'X': 1,
    'O': 2,
}

N_FICHA = [' ', 'X', 'O']
N_FICHA_CURRENT = ['·', 'X', 'O']


# 0 - Ningun jugador
# 1 - Jugador 1
# 2 - Jugador 2
class SubTablero:
    def __init__(self):
        self.tablero = np.zeros((3, 3), dtype=np.int8)
        self.ganador: int = 0

    def __getitem__(self, indices):
        """
        indices: np.ndarray de len() == 2
        """
        return self.tablero[indices]

    def casillas_libres(self):
        """
        Devuelve una lista de las posiciones libres en el tablero
        """
        if self.ganador == 0:
            return np.transpose(np.array(np.where(self.tablero == 0), dtype=np.int8))

        return []

    def casillas_ocupadas(self):
        """
        Devuelve una lista de las posiciones ocupadas en el tablero
        """
        return np.transpose(np.array(np.where(self.tablero != 0), dtype=np.int8))

    def jugar(self, jugador, row, col):
        """
        jugador: int
        row: int
        col: int
        Dado un jugador y una posicion (fila, columna), juega en la posicion dada
        """
        self.tablero[row, col] = jugador

        # Revisar si hay ganador
        # Por la columna
        if np.all(self.tablero[:, col] == jugador):
            self.ganador = jugador

        # Por la fila
        if np.all(self.tablero[row] == jugador):
            self.ganador = jugador

        # Por una diagonal
        if np.all(np.diag(self.tablero) == jugador):
            self.ganador = jugador

        # Por otra diagonal
        if np.all(np.diag(np.fliplr(self.tablero)) == jugador):
            self.ganador = jugador

        if np.all(self.tablero) and self.ganador == 0:
            self.ganador = None


class Tablero:
    def __init__(self):
        self.tableros = [SubTablero() for _ in range(9)]

        self.finalizado: bool = False

        self.jugada_anterior: np.ndarray = None

        # self.jugador: int = randint(1, 2)

    def __getitem__(self, indices):
        """
        indices: np.ndarray de len() == 2 or 4
        """
        if len(indices) == 2:
            return self.tableros[indices[0]*3 + indices[1]]
        elif len(indices) == 4:
            return self.tableros[indices[0]*3 + indices[1]][indices[2:]]

    def imprimir_tablero(self):
        """
        Imprime el tablero en la consola
        """
        # imprimir tablero en formato 9x9
        print("-"*25)
        for i in range(3):  
            string_fila_0 = "| "
            string_fila_1 = "| "
            string_fila_2 = "| "
            for j in range(3):

                if self.jugada_anterior is not None and self.jugada_anterior[0] == i and self.jugada_anterior[1] == j and self[self.jugada_anterior].ganador == 0:
                    symbols = N_FICHA_CURRENT
                else:
                    symbols = N_FICHA

                string_sub_fila_0 = [symbols[a] for a in self[i, j].tablero[0]]
                string_fila_0 += " ".join(string_sub_fila_0) + " | "

                string_sub_fila_1 = [symbols[a] for a in self[i, j].tablero[1]]
                string_fila_1 += " ".join(string_sub_fila_1) + " | "

                string_sub_fila_2 = [symbols[a] for a in self[i, j].tablero[2]]
                string_fila_2 += " ".join(string_sub_fila_2) + " | "
            print(string_fila_0)
            print(string_fila_1)
            print(string_fila_2)
            print("-"*25)

    def jugadas_disponibles(self):
        """
        Devuelve una lista de las posiciones disponibles en el tablero con
        elementos de la forma
        [(tablero_x, tablero_y, pos_en_tablero_x, pos_en_tablero_y))]
        """
        posibles = []

        # Si es el primer turno o no se ha registrado la posición de la jugada anterior
        # O el tablero que corresponde por la jugada anterior ya tiene un ganador
        if self.jugada_anterior is None or self[self.jugada_anterior].ganador != 0:
            positions = np.array(list(np.ndindex(3, 3)), dtype=np.int8)
            for pos in positions:
                for vacio in self[pos].casillas_libres():
                    # Si el sub tablero aún no tiene ganador
                    if self[pos].ganador == 0:
                        # Obtenemos las posiciones disponibles en el tablero
                        posibles.append(np.concatenate((pos, vacio)))

            return posibles
        else:
            # Si no es el primer turno y el tablero que corresponde por la jugada anterior
            # no tiene ganador, usamos la posición de la jugada anterior
            for vacio in self[self.jugada_anterior].casillas_libres():
                # Obtenemos las posiciones disponibles en el tablero
                posibles.append(np.concatenate((self.jugada_anterior, vacio)))

        return posibles

    def revisar_ganador(self):
        """
        Revisa si hay un ganador en el tablero
        """
        tablero = np.array([s.ganador for s in self.tableros]).reshape((3, 3))

        # Revisar si hay ganador por fila o columna
        for i in range(3):
            if np.all(tablero[i] == tablero[i][0]) and tablero[i][0] != 0:
                self.finalizado = True
                return N_FICHA[tablero[i][0]]
            if np.all(tablero[:, i] == tablero[0][i]) and tablero[0][i] != 0:
                self.finalizado = True
                return N_FICHA[tablero[0][i]]

        # Revisar si hay ganador por diagonal
        if np.all(np.diag(tablero) == tablero[0][0]) and tablero[0][0] != 0:
            self.finalizado = True
            return N_FICHA[tablero[0][0]]
        if np.all(np.diag(np.fliplr(tablero)) == tablero[0][2]) and tablero[0][2] != 0:
            self.finalizado = True
            return N_FICHA[tablero[0][2]]

        # Devuelve 0 si no hay ganador
        return 0

    def ejecutar_jugada(self, jugada: np.ndarray, ficha: str):
        """
        jugada: np.ndarray de len() == 4}
        posiciones: [subtablero_x, subtablero_y, pos_en_subtablero_x, pos_en_subtablero_y]
        """

        ficha = FICHA[ficha]

        # Si no hay una jugada anterior regustrada o el subtablero que toca ya tiene un ganador tiene un ganador
        # Se puede juga en cualquier subtablero
        if self.jugada_anterior is None or self[self.jugada_anterior].ganador != 0:
            # Se puede jugar en cualquier tablero que no tenga ganador (esta lógica la vemos en la clase
            # jugador)
            self[jugada[:2]].jugar(ficha, *jugada[2:])
        else:
            # Se juega en el subtablero indicado por la jugada anterior
            self[self.jugada_anterior].jugar(ficha, *jugada[2:])

        # Guardamos la posición de la jugada actual, para la siguiente jugada
        self.jugada_anterior = jugada[2:]


if __name__ == "__main__":
    juego = Tablero()
    juego.imprimir_tablero()
    print(juego.jugadas_disponibles())
    # juego.ejecutar_jugada(np.array([0,0,1,1]))
