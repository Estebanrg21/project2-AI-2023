from math import inf as infinity

from part1.entities.Board import Board


def minimax_ab(board: Board, depth, alpha, beta, is_max):
    is_game_over = board.has_winner()
    is_board_full = len(board.get_empty_nodes()) == 0
    if depth == 0 or is_game_over or is_board_full:
        return [None, board.score_position(1 if is_max else -1)]

    best = [None, -infinity] if is_max else [None, +infinity]

    empty_ones = board.get_empty_nodes()
    for child in empty_ones:
        if board.is_node_at_end(child):
            child.value = +1 if is_max else -1  # shrinks possibilities, fills empty fields
            eva = minimax_ab(board, depth - 1, alpha, beta, not is_max)
            if is_max:
                max_eva = max(eva[1], best[1])
                alpha = max(alpha, max_eva)
            else:
                min_eva = min(best[1], eva[1])
                beta = min(beta, min_eva)
            if eva[1] > best[1] and is_max or (eva[1] < best[1] and not is_max):
                eva[0] = child
                best = eva
            if beta <= alpha:
                break

    return best
