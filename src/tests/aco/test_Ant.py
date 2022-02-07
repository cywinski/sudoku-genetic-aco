import copy

import numpy as np

from src.aco.Ant import Ant
from src.aco.sudoku.SudokuBoard import SudokuBoard

TEST_BOARD = SudokuBoard(9)
TEST_ANT = Ant(np.random.default_rng(42), copy.deepcopy(TEST_BOARD), 0, None)


def test_get_board_index():
    assert (TEST_ANT._get_board_index(0) == (0, 0))
    assert (TEST_ANT._get_board_index(8) == (0, 8))
    assert (TEST_ANT._get_board_index(9) == (1, 0))
