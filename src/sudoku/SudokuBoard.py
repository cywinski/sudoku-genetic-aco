import math

import numpy as np

from .Cell import Cell


class SudokuBoard:
    def __init__(self, size: int) -> None:
        self.size = size
        self.board = np.array([[Cell(x, y) for y in range(self.size)] for x in range(self.size)])

    def init_cell_values(self, values_set: set) -> None:
        for value in values_set:
            self._set_cell_fixed_value(self.get_cell(value[0], value[1]), value[2])

    def read_from_file(self, filename: str) -> None:
        with open(filename, "r") as rf:
            for i, line in enumerate(rf):
                sudoku_row = line.rstrip()
                for j, num in enumerate(sudoku_row):
                    if int(num) != 0:
                        self._set_cell_fixed_value(self.get_cell(i, j), int(num))

    def _set_cell_fixed_value(self, cell: Cell, value: int) -> None:
        if cell.set_fixed_value(value):
            self._propagate_constraints(cell)

    def _eliminate_from_value_set(self, cell: Cell, value: int) -> None:
        if cell.eliminate(value):
            if cell.has_fixed_value():
                self._propagate_constraints(cell)

    @staticmethod
    def _get_fixed_values(cells: set) -> set:
        all_fixed_values = []
        for cell in cells:
            if cell.has_fixed_value():
                all_fixed_values.extend([v for v in cell.value_set])
        return set(all_fixed_values)

    def _propagate_constraints(self, cell: Cell) -> None:
        cell_peers = self.get_peers(cell)
        # 1) Eliminate from a cell’s value set all values that are fixed in
        # any of the cell’s peers
        for peer in cell_peers:
            self._eliminate_from_value_set(peer, cell.value_set.copy().pop())

            # 2) If any values in a cell’s value set are in the only possible
            # place in any of the cell’s units, then fix that value
            # for peer in cell_peers:
            for unit in [self.get_row_unit(peer), self.get_col_unit(peer), self.get_box_unit(peer)]:
                all_possible_values = [v for v in cell.value_set for cell in unit]
                for value in peer.value_set:
                    if value not in set(all_possible_values):
                        self._set_cell_fixed_value(cell, value)

    def get_cell(self, x: int, y: int) -> Cell:
        return self.board[x, y]

    def get_row_unit(self, cell: Cell) -> set:
        return set([c for c in self.board[cell.x, :] if (c.x != cell.x or c.y != cell.y)])

    def get_col_unit(self, cell: Cell) -> set:
        return set([c for c in self.board[:, cell.y] if (c.x != cell.x or c.y != cell.y)])

    def get_box_unit(self, cell: Cell) -> set:
        box_size = (int(math.sqrt(self.size)))
        box_start_row = (cell.x // box_size) * box_size
        box_start_col = (cell.y // box_size) * box_size
        return set(
            [c for c in self.board[box_start_row:box_start_row + 3, box_start_col:box_start_col + 3].flatten() if
             (c.x != cell.x or c.y != cell.y)])

    def get_peers(self, cell: Cell) -> set:
        return set.union(self.get_row_unit(cell), self.get_col_unit(cell), self.get_box_unit(cell))

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        self._board = value

    def __repr__(self) -> str:
        board_str = ""
        for row in range(self.size):
            if row % math.sqrt(self.size) == 0:
                board_str += "----------------------------------------------------------------------\n"

            for col in range(self.size):
                if col % math.sqrt(self.size) == 0:
                    board_str += "|"

                board_str += f"{self.get_cell(row, col)} "

            board_str += "|\n"

        board_str += "----------------------------------------------------------------------\n"
        return board_str
