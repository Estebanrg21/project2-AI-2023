import numpy as np

from part1.constants import COLUMN_COUNT, ROW_COUNT, WINDOW_LENGTH
from part1.entities.Node import Node


class Board(list):
    def __init__(self):
        super().__init__()
        [self.append([]) for _ in range(ROW_COUNT)]
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                self[row].append(Node(self, row, col))

    def is_node_at_end(self, node: Node):
        for row in range(ROW_COUNT - 1, -1, -1):
            if row > node.i and not self[row][node.j].value:
                return False
        return True

    def get_empty_nodes(self):
        _list = []
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                if self[row][col].is_empty():
                    node = self.adjust_choice_vertical(col)
                    if node:
                        _list.append(node)
        return _list

    def has_winner(self):
        return self.is_winning_move(1) or self.is_winning_move(-1)

    def is_winning_move(self, value):
        # Check valid horizontal locations for win
        for col in range(COLUMN_COUNT - 3):
            for row in range(ROW_COUNT):
                if self[row][col].value == value and \
                        self[row][col + 1].value == value and \
                        self[row][col + 2].value == value and self[row][col + 3].value == value:
                    return True

        # Check valid vertical locations for win
        for col in range(COLUMN_COUNT):
            for row in range(ROW_COUNT - 3):
                if self[row][col].value == value and \
                        self[row + 1][col].value == value and \
                        self[row + 2][col].value == value and \
                        self[row + 3][col].value == value:
                    return True

        # Check valid positive diagonal locations for win
        for col in range(COLUMN_COUNT - 3):
            for row in range(ROW_COUNT - 3):
                if self[row][col].value == value and \
                        self[row + 1][col + 1].value == value and \
                        self[row + 2][col + 2].value == value and \
                        self[row + 3][col + 3].value == value:
                    return True

        # check valid negative diagonal locations for win
        for col in range(COLUMN_COUNT - 3):
            for row in range(3, ROW_COUNT):
                if self[row][col].value == value and \
                        self[row - 1][col + 1].value == value and \
                        self[row - 2][col + 2].value == value and \
                        self[row - 3][col + 3].value == value:
                    return True

    def adjust_choice_vertical(self, col: int):
        selected_node = None
        for row in range(ROW_COUNT - 1, 0, -1):
            node = self[row][col - 1]
            if node.value is None:
                selected_node = node
                break
        if selected_node is not None:
            return selected_node

    def score_position(self, value):
        score = 0

        # Score centre column
        np_list = np.array(self)
        centre_array = [node.value for node in list(np_list[:, COLUMN_COUNT // 2])]
        centre_count = centre_array.count(value)
        score += centre_count * 3

        # Score horizontal positions
        for r in range(ROW_COUNT):
            row_array = [node.value for node in list(np_list[r, :])]
            for col in range(COLUMN_COUNT - 3):
                # Create a horizontal window of 4
                window = row_array[col:col + WINDOW_LENGTH]
                score += self.evaluate_window(window, value)

        # Score vertical positions
        for c in range(COLUMN_COUNT):
            col_array = [node.value for node in list(np_list[:, c])]
            for r in range(ROW_COUNT - 3):
                # Create a vertical window of 4
                window = col_array[r:r + WINDOW_LENGTH]
                score += self.evaluate_window(window, value)

        # Score positive diagonals
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                # Create a positive diagonal window of 4
                window = [self[r + i][c + i].value for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, value)

        # Score negative diagonals
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                # Create a negative diagonal window of 4
                window = [self[r + 3 - i][c + i].value for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, value)

        return score

    def evaluate_window(self, window, value):
        score = 0
        # Switch scoring based on turn
        opp_piece = -1
        if value == -1:
            opp_piece = 1

        if window.count(opp_piece) >= 1 and window.count(None) >= 1:
            score += 4
        # Prioritise a winning move
        elif window.count(value) == 4:
            score += 1
        # Make connecting 3 second priority
        elif window.count(value) == 3 and window.count(None) == 1:
            score += 2
        # Make connecting 2 third priority
        elif window.count(value) == 2 and window.count(None) == 2:
            score += 3

        return score
