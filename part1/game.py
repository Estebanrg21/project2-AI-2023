import copy
import random
import time
from math import inf

from algos.minimax import minimax, heuristic
from algos.minimax_ab import minimax_ab
from part1.constants import EMPTY_CHAR, ROW_COUNT, COLUMN_COUNT, AI_ID, USER_ID
from part1.entities.Board import Board


def render(board: Board, ai_choice, u_choice):
    chars = {
        -1: u_choice,
        +1: ai_choice,
        None: EMPTY_CHAR
    }
    str_line = '---------------' * 3

    print('\n' + str_line)

    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            symbol = chars[board[row][col].value]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)

def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print()
        print("Análisis:")
        print("-" * 30)
        print('El turno de la IA toma {:.3f} ms con un una profundidad de {:d}'.format((time2 - time1) * 1000.0, args[-1]))

        return ret

    return wrap


@timing
def ai_turn(board: Board, ai_choice, u_choice, use_minimax, _depth):
    depth = _depth
    print(f'Turno AI [{ai_choice}]')
    if depth == len(board.get_empty_nodes()):  # in case ai is first
        i = random.choice(range(ROW_COUNT))
        j = random.choice(range(COLUMN_COUNT))
        node = board[i][j]
    else:
        board_copy = copy.deepcopy(board)
        node, score = minimax(board_copy, depth, True) if use_minimax else \
            minimax_ab(board_copy, depth, -inf, +inf, True)
    if node is not None:
        board[node.i][node.j].value = +1
        if board.is_winning_move(1):
            print("Ha ganado la máquina!")
    else:
        result = heuristic(board)
        if result == -1:
            print("Felicidades usuario!")
        else:
            print("Ha ocurrido un empate!")
    render(board, ai_choice, u_choice)

def u_turn(board: Board, ai_choice, u_choice):
    print(f'Turno Usuario [{u_choice}]')
    render(board, ai_choice, u_choice)

    selected_col = 1
    while 0 <= selected_col - 1 < COLUMN_COUNT:
        selected_col = int(input(f"Seleccione la columna que desea utilizar (1 - {COLUMN_COUNT})"))
        selected_node = adjust_choice_vertical(board, selected_col - 1)
        selected_node.value = -1
        break


def adjust_choice_vertical(board: Board, col: int):
    selected_node = None
    for row in range(ROW_COUNT - 1, -1, -1):
        node = board[row][col]
        if node.value is None:
            selected_node = node
            break
    if selected_node is not None:
        return selected_node


option = None
menu = """
Bienvenid@ a 4 en linea
Elija el tipo de algoritmo que se desea utilizar
1 - minimax
2 - minimax alpha-beta
3 - salir
"""
while option != 3:
    option = int(input(menu))
    if option != 3:
        board = Board()
        profundidad = input("Ingrese profundidad del algoritmo: (Default 42 [6 filas * 7 columnas])")
        while len(board.get_empty_nodes()) > 0 and (not board.is_winning_move(+1) and not board.is_winning_move(-1)):
            u_turn(board, AI_ID, USER_ID)
            ai_turn(board, AI_ID, USER_ID, option == 1,
                    int(profundidad) if profundidad.isnumeric() else ROW_COUNT * COLUMN_COUNT)