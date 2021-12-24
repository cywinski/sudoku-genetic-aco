import copy
from random import randint

import numpy as np

from src.sudoku.SudokuBoard import SudokuBoard
from .Ant import Ant


class ACOSolver:
    def __init__(self,
                 board_size: int,
                 board_file: str,
                 num_ants: int,
                 max_iterations: int,
                 greediness: float,
                 pheromone_decay: float = 0.1,
                 evaporation_rate: float = 0.1,
                 best_evaporation_rate: float = 0.1) -> None:
        self.board_size = board_size
        self.board = SudokuBoard(self.board_size)
        self.board.read_from_file(board_file)  # read in puzzle and propagate constraints
        self.global_pheromone = self._init_global_pheromone()
        self.num_ants = num_ants
        self.max_iterations = max_iterations
        self.greediness = greediness
        self.pheromone_decay = pheromone_decay
        self.evaporation_rate = evaporation_rate
        self.best_evaporation_rate = best_evaporation_rate

    def _init_global_pheromone(self) -> np.ndarray:
        return np.full(shape=(self.board_size ** 2, 9), fill_value=1 / (self.board_size ** 2))

    def is_solved(self, current_iteration: int) -> bool:
        return current_iteration > self.max_iterations

    def _init_ants(self) -> list:
        # give each ant a local copy of Sudoku board and
        # assign each ant to a different random cell
        ants = []
        taken_positions = set()
        for m in range(self.num_ants):
            start_pos = randint(0, self.board_size ** 2 - 1)
            while start_pos in taken_positions:
                start_pos = randint(0, self.board_size ** 2 - 1)
            taken_positions.add(start_pos)
            ants.append(Ant(
                board_copy=copy.deepcopy(self.board),
                start_pos=start_pos,
                greediness=self.greediness,
                global_pheromone=self.global_pheromone,
                pheromone_decay=self.pheromone_decay
            ))
        return ants

    @staticmethod
    def _find_best_ant(ants):
        fixed_values_best = -np.inf
        iteration_best_ant = None
        for ant in ants:
            if ant.fixed_cells_number > fixed_values_best:
                fixed_values_best = ant.fixed_cells_number
                iteration_best_ant = ant
        return fixed_values_best, iteration_best_ant

    def _update_global_pheromone(self, best_pheromone_to_add: float, best_solution: Ant) -> None:
        self.global_pheromone[best_solution.pos - 1] = (1 - self.evaporation_rate) * self.global_pheromone[
            best_solution.pos - 1] + self.evaporation_rate * best_pheromone_to_add

    def _evaporate_best_value(self) -> None:
        best_pheromone = np.unravel_index(np.argmax(self.global_pheromone),
                                          shape=(self.board_size ** 2, self.board_size))
        self.global_pheromone[best_pheromone] = self.global_pheromone[best_pheromone] * (1 - self.best_evaporation_rate)

    def solve(self) -> Ant:
        i = 0
        best_pheromone_to_add = 0
        best_solution = None
        while not self.is_solved(i):
            ants = self._init_ants()
            for cell_num in range(self.board_size ** 2):
                for ant in ants:
                    ant.step()

            fixed_values_best, iteration_best_ant = self._find_best_ant(ants)
            pheromone_to_add = self.board_size ** 2 / (self.board_size ** 2 - fixed_values_best)
            if pheromone_to_add > best_pheromone_to_add:
                best_pheromone_to_add = pheromone_to_add
                best_solution = iteration_best_ant
                self._update_global_pheromone(pheromone_to_add, iteration_best_ant)

            self._evaporate_best_value()
            i += 1
        return best_solution
