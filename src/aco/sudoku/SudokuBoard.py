import itertools
import math

import numpy as np

from .Cell import Cell


class SudokuBoard:
    def __init__(self, size: int) -> None:
        self.size = size
        self.board = np.array([[Cell(x, y) for y in range(self.size)] for x in range(self.size)])
        self.num_fixed_cells = 0
        self.num_infeasible_cells = 0
        self.num_predefined_cells = 0

    def init_cell_values(self, values_set: set) -> None:
        for value in values_set:
            self.num_predefined_cells += 1
            self.set_cell_fixed_value(self.get_cell(value[0], value[1]), value[2])

    def read_from_file(self, filename: str) -> None:
        with open(filename, "r") as rf:
            for i, line in enumerate(rf):
                sudoku_row = line.rstrip()
                for j, num in enumerate(sudoku_row):
                    if int(num) != 0:
                        self.num_predefined_cells += 1
                        self.set_cell_fixed_value(self.get_cell(i, j), int(num))

    def set_cell_fixed_value(self, cell: Cell, value: int) -> None:
        if cell.has_fixed_value() or value not in cell.value_set:
            return

        cell.set_fixed_value(value)
        self.num_fixed_cells += 1
        self._propagate_constraints(cell)

    def eliminate_from_value_set(self, cell: Cell, value: int) -> None:
        if value in cell.value_set:
            cell.eliminate(value)
            if cell.has_fixed_value():
                self.num_fixed_cells += 1
                self._propagate_constraints(cell)

    def get_fixed_cells(self) -> list:
        fixed_cells = []
        for cell in self.board.flatten():
            if cell.has_fixed_value():
                fixed_cells.append(cell)
        return fixed_cells

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
            if not peer.is_failed() and not cell.is_failed():
                self.eliminate_from_value_set(peer, list(cell.value_set)[0])

        # 2) If any values in a cell’s value set are in the only possible
        # place in any of the cell’s units, then fix that value
        for peer in cell_peers:
            for unit in [self.get_row_unit(peer), self.get_col_unit(peer), self.get_box_unit(peer)]:
                if not peer.is_failed() and not peer.has_fixed_value():
                    all_possible_values = []
                    for c in unit:
                        for v in c.value_set:
                            all_possible_values.append(v)
                    for v in peer.value_set:
                        if v not in set(all_possible_values):
                            self.set_cell_fixed_value(peer, v)
                            break  # always max 1 value

        if cell.is_failed():
            self.num_infeasible_cells += 1

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

    @staticmethod
    def _is_row_correct(row: np.ndarray) -> bool:
        values = []
        for cell in row:
            if not cell.has_fixed_value():
                return False
            values.extend(list(cell.value_set))
        return len(values) == 9 and sum(values) == sum(set(values))

    def is_correct(self) -> bool:
        bad_rows = [row for row in self.board if not self._is_row_correct(row)]
        grid = list(zip(*self.board))
        bad_cols = [col for col in grid if not self._is_row_correct(np.array(col))]
        squares = []
        for i in range(self.size, 3):
            for j in range(self.size, 3):
                square = list(itertools.chain(row[j:j + 3] for row in grid[i:i + 3]))
                squares.append(square)
        bad_squares = [square for square in squares if not self._is_row_correct(np.array(square))]
        return not (bad_rows or bad_squares or bad_cols)

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
                board_str += "----------------------\n"

            for col in range(self.size):
                if col % math.sqrt(self.size) == 0:
                    board_str += "|"

                board_str += f"{self.get_cell(row, col)} "

            board_str += "|\n"

        board_str += "----------------------\n"
        return board_str
