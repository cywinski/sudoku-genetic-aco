from typing import Tuple

import numpy as np

from src.aco.sudoku import Cell
from src.aco.sudoku.SudokuBoard import SudokuBoard


class Ant:
    def __init__(self, board_copy: SudokuBoard, start_pos: int, parent) -> None:
        self.board = board_copy
        self.pos = start_pos
        self.failed_cells_count = 0
        self.parent = parent

    def get_num_cells_filled(self):
        return self.board.num_fixed_cells - self.failed_cells_count

    def _get_board_index(self, pos: int) -> Tuple[np.ndarray]:
        return np.unravel_index(pos, shape=(self.board.size ** 2, self.board.size))

    def _choose_value_from_value_set(self, current_cell: Cell) -> int:

        if np.random.uniform() > self.parent.greediness:
            # greedy selection
            choice = np.array(list(current_cell.value_set))[
                np.argmax(self.parent.pheromone[self.pos - 1][np.array(list(current_cell.value_set)) - 1])]
        else:
            # roulette wheel selection
            prob_distribution = [
                    pheromone / np.sum(self.parent.pheromone[self.pos - 1][np.array(list(current_cell.value_set)) - 1])
                    for pheromone in self.parent.pheromone[self.pos - 1][np.array(list(current_cell.value_set)) - 1]]
            choice = np.random.choice(a=list(current_cell.value_set), p=prob_distribution)
        return choice

    def _move_to_next_cell(self) -> None:
        self.pos = (self.pos + 1) % (self.board.size ** 2 - 1)

    def step(self) -> None:
        current_cell = self.board.get_cell(*self._get_board_index(self.pos))

        if current_cell.is_failed():
            self.failed_cells_count += 1
        elif not current_cell.has_fixed_value():
            choice = self._choose_value_from_value_set(current_cell)
            self.board.set_cell_fixed_value(current_cell, choice)
            self.parent.update_local_pheromone(self.pos, choice)

        self._move_to_next_cell()
