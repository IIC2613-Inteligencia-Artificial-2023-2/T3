def contar_tableros_diferencia(tablero, ficha) -> int:
    """
    tablero: Tablero
    jugador: int
    Devuelve la cantidad de subtableros en que el jugador tiene más fichas que el oponente
    """
    tableros_con_diferencia = 0
    for sub_tablero in tablero.tableros:
        contar_ficha_1 = 0
        contar_ficha_2 = 0
        for a in range(3):
            for i in range(3):
                if sub_tablero[a, i] == 1:
                    contar_ficha_1 += 1
                elif sub_tablero[a, i] == 2:
                    contar_ficha_2 += 1
        if ficha == 1 and contar_ficha_1 > contar_ficha_2:
            tableros_con_diferencia += 1
        elif ficha == 2 and contar_ficha_2 > contar_ficha_1:
            tableros_con_diferencia += 1
    return tableros_con_diferencia


def contar_fichas_seguidas(tablero, ficha) -> int:
    """
    tablero: Tablero
    ficha: int
    Devuelve la cantidad de pares de fichas seguidas de un jugador, se suma 3
    si tiene 3 seguidas (ganador del tablero)
    """
    # TODO: IMPLEMENTAR
