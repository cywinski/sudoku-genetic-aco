import copy
import time

import numpy as np

from src.aco.sudoku.SudokuBoard import SudokuBoard
from .Ant import Ant


class ACOSolver:
    def __init__(
            self, random_generator, board_size: int, board_file: str, num_ants: int, max_iterations: int,
            greediness: float,
            pheromone_decay: float = 0.1, evaporation_rate: float = 0.9,
            best_evaporation_rate: float = 0.005
            ) -> None:
        self.rng = random_generator  # random generator to use while using np.random
        self.board_size = board_size
        self.board = SudokuBoard(self.board_size)
        self.board.read_from_file(board_file)  # read in puzzle and propagate constraints
        self.pheromone = self._init_pheromone()
        self.num_ants = num_ants
        self.max_iterations = max_iterations
        self.greediness = greediness
        self.pheromone_decay = pheromone_decay
        self.evaporation_rate = evaporation_rate
        self.best_evaporation_rate = best_evaporation_rate
        self.best_board = self.board
        self.solution_time = 0

    def _init_pheromone(self) -> np.ndarray:
        return np.full(shape=(self.board_size ** 2, 9), fill_value=1 / (self.board_size ** 2))

    def is_solved(self, current_iteration: int) -> bool:
        return current_iteration > self.max_iterations and self.best_board.is_correct()

    def _init_ants(self) -> list:
        # give each ant a local copy of Sudoku board and
        # assign each ant to a different random cell
        ants = []
        positions = np.arange(0, self.board_size ** 2 - 1)
        self.rng.shuffle(positions)  # shuffled positions on board

        for m in range(self.num_ants):
            start_pos = positions[m % len(positions)]
            ants.append(
                Ant(random_generator=self.rng, board_copy=copy.deepcopy(self.board), start_pos=start_pos, parent=self))
        return ants

    @staticmethod
    def _find_best_ant(ants: list[Ant]):
        fixed_values_best = -np.inf
        iteration_best_ant = None
        for ant in ants:
            if ant.board.num_fixed_cells - ant.board.num_infeasible_cells - ant.failed_cells_count - ant.board.num_predefined_cells > fixed_values_best:
                fixed_values_best = ant.board.num_fixed_cells - ant.board.num_infeasible_cells - ant.failed_cells_count - ant.board.num_predefined_cells
                iteration_best_ant = ant
        return fixed_values_best, iteration_best_ant

    def update_local_pheromone(self, pos: int, selection: int) -> None:
        self.pheromone[pos - 1][selection - 1] = (self.pheromone[pos - 1][selection - 1] * self.evaporation_rate) + (
                1 / (self.board_size ** 2)) * self.pheromone_decay

    def _update_pheromone(self, best_pheromone_to_add: float) -> None:
        for i in range(self.board_size ** 2):
            cell = self.best_board.get_cell(*np.unravel_index(i, shape=(self.board.size ** 2, self.board.size)))
            if cell.has_fixed_value():
                self.pheromone[i][list(cell.value_set)[0] - 1] = (1 - self.evaporation_rate) * self.pheromone[i][
                    list(cell.value_set)[0] - 1] + self.evaporation_rate * best_pheromone_to_add

    def solve(self, logging=True):
        # To statistics
        all_fixed_values_best = []
        all_pheromones_to_add = []
        all_perc_fixed_cells = []
        all_iterations = []

        i = 0
        best_pheromone_to_add = 0
        best_ant = None
        solved = False
        start = time.time()
        while not solved and i < self.max_iterations:
            ants = self._init_ants()
            for cell_num in range(self.board_size ** 2):
                for ant in ants:
                    ant.step()

            # update pheromone
            fixed_values_best, iteration_best_ant = self._find_best_ant(ants)
            pheromone_to_add = self.board_size ** 2 / (self.board_size ** 2 - fixed_values_best)
            if pheromone_to_add > best_pheromone_to_add:
                # new best
                self.best_board = copy.deepcopy(iteration_best_ant.board)
                best_pheromone_to_add = pheromone_to_add
                best_ant = iteration_best_ant
                if fixed_values_best == self.board_size ** 2 - self.board.num_predefined_cells:
                    solved = True
                    self.solution_time = time.time() - start

            self._update_pheromone(best_pheromone_to_add)
            best_pheromone_to_add *= (1.0 - self.evaporation_rate)
            if logging:
                print(
                        f"Iteration: {i + 1} Fixed cells %: {(len(best_ant.board.get_fixed_cells()) / best_ant.board.size ** 2) * 100:.2f} Pheromone to add: {pheromone_to_add:.3f}")

            all_fixed_values_best.append(fixed_values_best)
            all_pheromones_to_add.append(pheromone_to_add)
            all_perc_fixed_cells.append((len(best_ant.board.get_fixed_cells()) / best_ant.board.size ** 2) * 100)
            all_iterations.append(i)

            i += 1

        return solved, all_fixed_values_best, all_pheromones_to_add, all_perc_fixed_cells, all_iterations
