import copy
import math
import random
from typing import List

from src.genetic_algorithm.individual.Individual import Individual, is_ok_mini_board


class GASolver:
    def __init__(self, board_path: str, population_size: int = 1000, number_generations: int = 1000,
                 sudoku_shape: int = 9, mutation_probability: float = 0.5, elite_param: int = 2,
                 tournament_size: int = 3, cross_probability: float = 0.5, cataclystic_ratio: int = 5000,
                 print_rate: int = 10):
        self.population_size = population_size
        self.number_generations = number_generations
        self.sudoku_shape = sudoku_shape
        self.board_path = board_path
        self.elite_param = elite_param
        self.mutation_probability = mutation_probability
        self.tournament_size = tournament_size
        self.cross_probability = cross_probability
        self.cataclystic_ratio = cataclystic_ratio
        self.population = []
        self.auxiliary_individual = Individual(sudoku_shape=self.sudoku_shape)
        self.print_rate = print_rate
        self._number_iterations = 0
        self._loss_fun_executions = 0
        self._number_reinitializations = 0

    def _init_population(self):
        self.population.clear()
        for _ in range(self.population_size):
            self.population.append(Individual(sudoku_shape=self.sudoku_shape))

    def init_auxiliary(self):
        self.auxiliary_individual.init_from_file(path=self.board_path)

    def initialize_population(self):
        self.population.clear()
        for _ in range(self.population_size):
            individual = Individual(sudoku_shape=self.sudoku_shape)
            individual.init_from_file(path=self.board_path)
            individual.create_with_shuffle()
            self.population.append(individual)

    def perform_cross(self):
        working_population1 = copy.deepcopy(self.population)
        working_population2 = copy.deepcopy(self.population)
        first_parent_group = random.sample(working_population1, self.tournament_size)
        second_parent_group = random.sample(working_population2, self.tournament_size)
        first_parent_group.sort(key=lambda x: x.rating)
        second_parent_group.sort(key=lambda x: x.rating)
        first_parent = first_parent_group[0]
        second_parent = second_parent_group[0]
        if random.random() < self.cross_probability:
            place_of_partition = random.randint(1, 8)

            new_first_parent = Individual(sudoku_shape=self.sudoku_shape)
            new_second_parent = Individual(sudoku_shape=self.sudoku_shape)
            for index in range(len(first_parent.board)):
                if index < place_of_partition:
                    new_first_parent.board.append(first_parent.board[index])
                    new_second_parent.board.append(second_parent.board[index])
                else:
                    new_first_parent.board.append(second_parent.board[index])
                    new_second_parent.board.append(first_parent.board[index])
            if new_first_parent.is_board_ok_in_mini_boards() is False or \
                    new_second_parent.is_board_ok_in_mini_boards() is False:
                raise Exception("Mini-boards are wrong!")
            for index in range(len(new_first_parent.board)):
                if is_ok_mini_board(current=new_first_parent.board[index],
                                    original=self.auxiliary_individual.board[index]) is False or \
                        is_ok_mini_board(current=new_second_parent.board[index],
                                         original=self.auxiliary_individual.board[index]) is False:
                    raise Exception("Mini-boards dont match starting board!")
            return new_first_parent, new_second_parent
        else:
            return first_parent, second_parent

    def rate_population(self):
        for individual in self.population:
            individual.rate()
            self._loss_fun_executions += 1

    def sort_population(self):
        # assuming population is rated!
        self.population.sort(key=lambda x: x.rating, reverse=False)

    def is_sudoku_solved(self):
        # assuming population is rated and sorted
        if len(self.population) == 0 or self.population[0].rating is None:
            raise Exception("Solver has no population or population is not rated")
        return self.population[0].rating == 0

    def elite_succession(self, new_population: List[List]):
        for index in range(self.elite_param):
            new_population.append(self.population[index])
        return new_population

    def give_penalty_to_best(self, best_so_far_board: List[List] = None):
        if best_so_far_board and best_so_far_board == self.population[0].board:
            self.population[0].rating += 1
            self.sort_population()
        best_so_far_board = copy.deepcopy(self.population[0].board)
        return best_so_far_board

    def _reset_statistics(self):
        self._number_iterations = 0
        self._loss_fun_executions = 0
        self._number_reinitializations = 0

    def show_statistics(self):
        print(
            f"Number of iterations performed: {self._number_iterations}\n"
            f"Number of loss function executions: {self._loss_fun_executions}\n"
            f"Number of reinitializations of population: {self._number_reinitializations}\n"
        )

    def solve(self):
        self._reset_statistics()
        best_so_far_board = None

        while True:
            # possible reinitialization
            if self._number_iterations % self.cataclystic_ratio == 0 and self._number_iterations != 0:
                self._number_reinitializations += 1
                print(f"~~~~Reinitialization {self._number_reinitializations}~~~~")
                self.initialize_population()

            # rate population by fitness and sort
            self.rate_population()
            self.sort_population()

            # additional penalty if best solution from previous generation is same with current best solution
            best_so_far_board = self.give_penalty_to_best(best_so_far_board=best_so_far_board)
            if self._number_iterations % self.print_rate == 0:
                print(f"On generation {self._number_iterations} best individual rate={self.population[0].rating}")

            # check stop criterion
            if self.is_sudoku_solved():
                return self.population[0]

            # create new population with elite_succession, cross and mutation
            new_population = []
            new_population = self.elite_succession(new_population=new_population)
            while len(new_population) != self.population_size:
                individual1, individual2 = self.perform_cross()
                individual1.mutate(comparator=self.auxiliary_individual.board,
                                   mutation_probability=self.mutation_probability)
                individual2.mutate(comparator=self.auxiliary_individual.board,
                                   mutation_probability=self.mutation_probability)
                new_population.append(individual1)
                new_population.append(individual2)

            self.population = new_population
            self._number_iterations += 1
