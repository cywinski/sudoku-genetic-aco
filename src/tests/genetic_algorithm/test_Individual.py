import copy
import random

import pytest

from src.genetic_algorithm.individual.Individual import Individual, is_ok_mini_board

random.seed(120)

def test_adding():
    assert 1 + 1 == 2


def test_create_object():
    individual = Individual()
    assert individual is not None


def test_individual_init():
    individual = Individual()
    assert individual.sudoku_shape == 9
    individual = Individual(15)
    assert individual.sudoku_shape == 15


def test_init_from_file():
    individual = Individual()
    resp = individual.init_from_file("fake_path.txt")
    assert resp is False
    assert len(individual.board) == 0
    resp = individual.init_from_file("src/tests/genetic_algorithm/test_board_starting.txt")
    assert resp is True
    ok_board = [[0, 6, 0, 0, 3, 0, 0, 2, 0], [0, 0, 0, 0, 0, 7, 3, 0, 6], [5, 0, 2, 0, 0, 0, 0, 0, 7],
                [8, 7, 3, 9, 4, 0, 0, 1, 0], [0, 2, 1, 5, 0, 0, 0, 0, 4], [4, 5, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 3, 9, 4, 0, 5, 1], [0, 9, 5, 8, 1, 0, 0, 6, 3], [0, 0, 4, 0, 7, 5, 0, 9, 8]]
    for mini_board_target, ind_board in zip(ok_board, individual.board):
        for x, y in zip(mini_board_target, ind_board):
            assert x == y


def test_create_with_shuffle():
    individual = Individual()
    assert individual.create_with_shuffle() is False
    individual.init_from_file(path="src/tests/genetic_algorithm/test_board_starting.txt")
    ok_board = individual.board
    assert individual.create_with_shuffle() is True
    for board_before, board_after in zip(ok_board, individual.board):
        for x, y in zip(board_before, board_after):
            if x == 0:
                assert x != y


def test_is_board_ok_in_mini_boards():
    individual = Individual()
    individual.board = [[0, 6, 0, 0, 3, 0, 0, 2, 0], [0, 0, 0, 0, 0, 7, 3, 0, 6], [5, 0, 2, 0, 0, 0, 0, 0, 7],
                        [8, 7, 3, 9, 4, 0, 0, 1, 0], [0, 2, 1, 5, 0, 0, 0, 0, 4], [4, 5, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 3, 9, 4, 0, 5, 1], [0, 9, 5, 8, 1, 0, 0, 6, 3], [0, 0, 4, 0, 7, 5, 0, 9, 8]]
    with pytest.raises(Exception):
        assert individual.is_board_ok_in_mini_boards() is False
    mini_board = [x for x in range(1, 10)]
    individual.board = [mini_board for _ in range(9)]
    assert individual.is_board_ok_in_mini_boards() is True
    individual.board[0][0] = 6
    assert individual.is_board_ok_in_mini_boards() is False


def test_is_ok_mini_board():
    mini_board_orig = [7, 2, 0, 0, 0, 5, 6, 1, 9]
    mini_board_ok = [7, 2, 4, 8, 3, 5, 6, 1, 9]
    mini_board_wrong = [2, 7, 4, 8, 3, 5, 6, 1, 9]
    with pytest.raises(Exception):
        assert is_ok_mini_board(mini_board_orig, mini_board_orig) is True
    assert is_ok_mini_board(mini_board_ok, mini_board_orig) is True
    assert is_ok_mini_board(mini_board_wrong, mini_board_orig) is False


def test_mutate():
    individual = Individual()
    individual.init_from_file(path="src/tests/genetic_algorithm/test_board_starting.txt")
    board_comparator = copy.deepcopy(individual.board)
    individual.create_with_shuffle()
    board_before = copy.deepcopy(individual.board)
    individual.mutate(comparator=board_comparator, mutation_probability=0.0)
    for mini_board_before, mini_board_current in zip(board_before, individual.board):
        assert mini_board_before == mini_board_current
    individual.mutate(comparator=board_comparator, mutation_probability=1.0)
    found_different = False
    for mini_board_before, mini_board_current in zip (board_before, individual.board):
        if mini_board_before != mini_board_current:
            found_different = True
    assert found_different is True


def test_rating():
    individual = Individual()
    individual.init_from_file(path="src/tests/genetic_algorithm/test_board_wrong.txt")
    individual.rate()
    assert individual.rating == 41
    individual.init_from_file(path="src/tests/genetic_algorithm/test_board_correct.txt")
    individual.rate()
    assert individual.rating == 0

