from board import Board
from solver import Solver
import sys

solver = None
board = None
if sys.argv[1] == "astar" and len(sys.argv) == 5:
    heuristic = sys.argv[3]
    # Revisamos que la heuristica sea valida
    if heuristic not in ["h0", "h1", "h2", "h3"]:
        print("Invalid heuristic")
        exit(1)
    weight = sys.argv[4]
    # Revisamos que el peso sea valido
    if not weight.replace('.', '', 1).isdigit():
        print("Invalid weight")
        exit(1)
    # Cargamos el tablero
    board = Board.readFromfile(sys.argv[2])
    print("Board inicial:")
    print(board.prettify(board.cars))
    # Inicializamos el solver
    solver = Solver(board, heuristic, float(weight))
    # Resolvemos el tablero
    final_node = solver.search()
    # Revisamos si se encontro una solucion
    if final_node is None:
        print("No solution")
    else:
        moves = final_node.trace()

else:
    print("Uso para A* : python rushhour/run.py astar <board> <heuristic> <weight>")
    exit(1)

# Imprimimos los movimientos
print(solver.solution(board, moves))
print(f'Found a solution in', len(moves), 'moves!')
print('Time: {} seconds'.format(solver.end_time - solver.start_time))
print('Expansions: {}'.format(solver.expansions))