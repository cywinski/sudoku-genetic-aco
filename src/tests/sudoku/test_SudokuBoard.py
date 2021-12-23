from src.sudoku.Cell import Cell
from src.sudoku.SudokuBoard import SudokuBoard

TEST_VALUES_SET = {
    (0, 1, 6),
    (0, 6, 5),
    (0, 8, 2),
    (1, 1, 3),
    (1, 5, 7),
    (2, 1, 2),
    (2, 3, 3),
    (2, 5, 6),
    (2, 8, 7),
    (3, 0, 8),
    (3, 1, 7),
    (3, 2, 3),
    (3, 4, 2),
    (3, 5, 1),
    (3, 6, 4),
    (3, 7, 5),
    (4, 0, 9),
    (4, 1, 4),
    (4, 3, 5),
    (5, 1, 1),
    (5, 5, 4),
    (6, 4, 9),
    (6, 5, 5),
    (6, 8, 4),
    (7, 0, 3),
    (7, 1, 9),
    (7, 2, 4),
    (7, 3, 8),
    (7, 4, 1),
    (7, 7, 7),
    (7, 8, 5),
    (8, 1, 5),
    (8, 2, 1),
    (8, 4, 6),
    (8, 5, 3),
    (8, 7, 9),
    (8, 8, 8)
}
TEST_BOARD = SudokuBoard(9)
TEST_CELL = Cell(7, 2)


def test_init_cell_values():
    TEST_BOARD.init_cell_values(TEST_VALUES_SET)
    expected_result = [
        [{4}, {6}, {7}, {1}, {8}, {9}, {5}, {3}, {2}],
        [{1, 5}, {3}, {5, 8, 9}, {2}, {4, 5}, {7}, {1, 8, 9}, {4, 6, 8}, {1, 6, 9}],
        [{1, 5}, {2}, {5, 8, 9}, {3}, {4, 5}, {6}, {1, 8, 9}, {4, 8}, {7}],
        [{8}, {7}, {3}, {6, 9}, {2}, {1}, {4}, {5}, {6, 9}],
        [{9}, {4}, {2, 6}, {5}, {3, 7}, {8}, {1, 7}, {2, 6}, {1, 3, 6}],
        [{2, 5, 6}, {1}, {2, 5, 6}, {6, 9}, {3, 7}, {4}, {7, 8, 9}, {2, 6, 8}, {3, 6, 9}],
        [{2, 6}, {8}, {2, 6}, {7}, {9}, {5}, {3}, {1}, {4}],
        [{3}, {9}, {4}, {8}, {1}, {2}, {6}, {7}, {5}],
        [{7}, {5}, {1}, {4}, {6}, {3}, {2}, {9}, {8}]
    ]
    result = []
    for row in TEST_BOARD.board:
        result.append([cell.value_set for cell in row])

    assert (TEST_BOARD.get_cell(0, 1).value_set == {6})
    assert (TEST_BOARD.get_cell(7, 2).value_set == {4})
    assert (expected_result == result)


def test_read_from_file():
    TEST_BOARD.read_from_file("../../../resources/boards/board1.txt")
    expected_result = [
        [{4}, {6}, {7}, {1}, {8}, {9}, {5}, {3}, {2}],
        [{1, 5}, {3}, {5, 8, 9}, {2}, {4, 5}, {7}, {1, 8, 9}, {4, 6, 8}, {1, 6, 9}],
        [{1, 5}, {2}, {5, 8, 9}, {3}, {4, 5}, {6}, {1, 8, 9}, {4, 8}, {7}],
        [{8}, {7}, {3}, {6, 9}, {2}, {1}, {4}, {5}, {6, 9}],
        [{9}, {4}, {2, 6}, {5}, {3, 7}, {8}, {1, 7}, {2, 6}, {1, 3, 6}],
        [{2, 5, 6}, {1}, {2, 5, 6}, {6, 9}, {3, 7}, {4}, {7, 8, 9}, {2, 6, 8}, {3, 6, 9}],
        [{2, 6}, {8}, {2, 6}, {7}, {9}, {5}, {3}, {1}, {4}],
        [{3}, {9}, {4}, {8}, {1}, {2}, {6}, {7}, {5}],
        [{7}, {5}, {1}, {4}, {6}, {3}, {2}, {9}, {8}]
    ]
    result = []
    for row in TEST_BOARD.board:
        result.append([cell.value_set for cell in row])

    assert (TEST_BOARD.get_cell(0, 1).value_set == {6})
    assert (TEST_BOARD.get_cell(7, 2).value_set == {4})
    assert (expected_result == result)


def test_get_row_unit():
    expected_row_unit = {(7, y) for y in range(9) if y != 2}

    row_unit = {(cell.x, cell.y) for cell in TEST_BOARD.get_row_unit(TEST_CELL)}

    assert (len(row_unit) == 8)
    assert (row_unit == expected_row_unit)


def test_get_col_unit():
    expected_col_unit = {(x, 2) for x in range(9) if x != 7}

    col_unit = {(cell.x, cell.y) for cell in TEST_BOARD.get_col_unit(TEST_CELL)}

    assert (len(col_unit) == 8)
    assert (col_unit == expected_col_unit)


def test_get_box_unit():
    expected_box_unit = {(6, 0), (6, 1), (6, 2),
                         (7, 0), (7, 1),
                         (8, 0), (8, 1), (8, 2)}
    box_unit = {(cell.x, cell.y) for cell in TEST_BOARD.get_box_unit(TEST_CELL)}
    assert (len(box_unit) == 8)
    assert (box_unit == expected_box_unit)


def test_get_peers():
    expected_peers = set.union({(7, y) for y in range(9) if y != 2}, {(x, 2) for x in range(9) if x != 7},
                               {(6, 0), (6, 1), (6, 2),
                                (7, 0), (7, 1),
                                (8, 0), (8, 1), (8, 2)})
    peers = {(cell.x, cell.y) for cell in TEST_BOARD.get_peers(TEST_CELL)}

    assert (len(peers) == 20)
    assert (peers == expected_peers)
