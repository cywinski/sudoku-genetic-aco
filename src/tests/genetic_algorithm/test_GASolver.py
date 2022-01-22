import copy
import random

from src.genetic_algorithm.GASolver import GASolver
from src.genetic_algorithm.individual.Individual import Individual

TEST_BOARD_PATH_1 = "src/tests/genetic_algorithm/test_board_starting.txt"
TEST_BOARD_SOLVED_PATH = "src/tests/genetic_algorithm/solved_sudoku.txt"
random.seed(110)

def test_adding():
    assert 1 + 1 == 2


def test_create_object():
    solver = GASolver(board_path=TEST_BOARD_PATH_1)
    assert solver is not None


def test_solver_init():
    solver = GASolver(board_path=TEST_BOARD_PATH_1)
    assert solver.population_size == 1000
    assert solver.number_generations == 1000
    solver2 = GASolver(board_path=TEST_BOARD_PATH_1, population_size=5, number_generations=12)
    assert solver2.population_size == 5
    assert solver2.number_generations == 12


def test_population_init():
    solver = GASolver(board_path=TEST_BOARD_PATH_1)
    assert len(solver.population) == 0
    solver._init_population()
    assert len(solver.population) == solver.population_size


def test_init_auxiliary():
    solver = GASolver(board_path=TEST_BOARD_PATH_1)
    assert len(solver.auxiliary_individual.board) == 0
    solver.init_auxiliary()
    ok_board = [[0, 6, 0, 0, 3, 0, 0, 2, 0], [0, 0, 0, 0, 0, 7, 3, 0, 6], [5, 0, 2, 0, 0, 0, 0, 0, 7],
                [8, 7, 3, 9, 4, 0, 0, 1, 0], [0, 2, 1, 5, 0, 0, 0, 0, 4], [4, 5, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 3, 9, 4, 0, 5, 1], [0, 9, 5, 8, 1, 0, 0, 6, 3], [0, 0, 4, 0, 7, 5, 0, 9, 8]]
    for mini_board_target, ind_board in zip(ok_board, solver.auxiliary_individual.board):
        for x, y in zip(mini_board_target, ind_board):
            assert x == y


def test_initialize_population():
    solver = GASolver(board_path=TEST_BOARD_PATH_1, population_size=50)
    assert len(solver.population) == 0
    solver.initialize_population()
    assert len(solver.population) == 50
    for individual in solver.population:
        assert individual.is_board_ok_in_mini_boards() is True


def test_is_solved():
    solver = GASolver(board_path="", population_size=1, number_generations=1)
    individual = Individual()
    individual.init_from_file(path=TEST_BOARD_SOLVED_PATH)
    solver.population.append(individual)
    solver.rate_population()
    assert solver.is_sudoku_solved() is True


def test_elite_succession():
    solver = GASolver(board_path=TEST_BOARD_PATH_1, population_size=5, elite_param=3)
    solver.initialize_population()
    assert len(solver.population) == 5
    new_population = []
    new_population = solver.elite_succession(new_population)
    assert len(new_population) == 3


def test_sort():
    solver = GASolver(board_path=TEST_BOARD_PATH_1, population_size=35)
    solver.initialize_population()
    solver.rate_population()
    solver.sort_population()
    for next_index in range(1, len(solver.population)):
        assert solver.population[next_index].rating >= solver.population[next_index-1].rating


def test_cross():
    solver = GASolver(board_path=TEST_BOARD_PATH_1, population_size=35, cross_probability=1)
    solver.initialize_population()
    solver.init_auxiliary()
    solver.rate_population()
    solver.sort_population()
    par_1, par_2 = solver.perform_cross()

    boards = [ind.board for ind in solver.population]
    assert par_1.board not in boards
    assert par_2.board not in boards

    solver.cross_probability = 0.0
    par_1, par_2 = solver.perform_cross()
    assert par_1.board in boards
    assert par_2.board in boards

