from typing import Tuple

import numpy as np

from src.aco.sudoku import Cell
from src.aco.sudoku.SudokuBoard import SudokuBoard


class Ant:
    def __init__(self, board_copy: SudokuBoard, start_pos: int, greediness: float,
                 global_pheromone: np.ndarray, pheromone_decay: float) -> None:
        self.board = board_copy
        self.pos = start_pos
        self.greediness = greediness
        self.pheromone = global_pheromone
        self.pheromone_decay = pheromone_decay
        self.failed_cells_count = 0
        self.fixed_cells_number = 0

    def _get_board_index(self, pos: int) -> Tuple[np.ndarray]:
        return np.unravel_index(pos, shape=(self.board.size ** 2, self.board.size))

    def _choose_value_from_value_set(self, current_cell: Cell) -> int:
        if np.random.uniform() < self.greediness:
            # greedy selection
            selection = np.array(list(current_cell.value_set))[
                np.argmax(self.pheromone[self.pos - 1][np.array(list(current_cell.value_set)) - 1])]
        else:
            # roulette wheel selection
            prob_distribution = [
                pheromone / np.sum(self.pheromone[self.pos - 1][np.array(list(current_cell.value_set)) - 1])
                for pheromone in self.pheromone[self.pos - 1][np.array(list(current_cell.value_set)) - 1]]
            selection = np.random.choice(a=list(current_cell.value_set), p=prob_distribution)
        return selection

    def _update_local_pheromone(self, selection: int) -> None:
        self.pheromone[self.pos - 1][selection - 1] = (1 - self.pheromone_decay) * self.pheromone[self.pos - 1][
            selection - 1] + self.pheromone_decay * (1 / (self.board.size ** 2))

    def _move_to_next_cell(self) -> None:
        self.pos = (self.pos + 1) % (self.board.size ** 2 - 1)

    def step(self) -> None:
        current_cell = self.board.get_cell(*self._get_board_index(self.pos))
        if not current_cell.has_fixed_value() and not current_cell.is_failed():
            selection = self._choose_value_from_value_set(current_cell)
            self.board.set_cell_fixed_value(current_cell, selection)
            self._update_local_pheromone(selection)
            self.fixed_cells_number += 1
        elif current_cell.is_failed():
            self.failed_cells_count += 1

        self._move_to_next_cell()
