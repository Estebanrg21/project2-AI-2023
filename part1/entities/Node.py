class Node:

    def __init__(self, board, i: int, j: int, value=None):
        self.board = board
        self.value = value
        self.i = i
        self.j = j

    def is_empty(self):
        return self.value is None

    def __repr__(self):
        return f"{self.value}"
