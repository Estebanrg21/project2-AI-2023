from math import inf as infinity

import copy
from part1.entities.Board import Board


def heuristic(board: Board):
    if board.is_winning_move(+1):
        score = +1
    elif board.is_winning_move(-1):
        score = -1
    else:
        score = 0
    return score


def minimax(board: Board, depth, is_max):
    is_game_over = board.has_winner()
    is_board_full = len(board.get_empty_nodes()) == 0
    if depth == 0 or is_game_over or is_board_full:
        return [None, board.score_position(1 if is_max else -1)]

    best = [None, -infinity] if is_max else [None, +infinity]

    empty_ones = board.get_empty_nodes()
    for child in empty_ones:
        if board.is_node_at_end(child):
            child.value = +1 if is_max else -1  # shrinks possibilities, fills empty fields
            score = minimax(board, depth - 1, not is_max)
            if score[1] > best[1] and is_max or (score[1] < best[1] and not is_max):
                score[0] = child
                best = score

    return best
