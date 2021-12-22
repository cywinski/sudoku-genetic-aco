from src.sudoku.Cell import Cell

TEST_CELL = Cell(0, 0)


def test_create_cell():
    cell = Cell(0, 0)

    assert (cell.x == 0)
    assert (cell.y == 0)
    assert (cell.value_set == {1, 2, 3, 4, 5, 6, 7, 8, 9})


def test_set_fixed_value_success():
    cell = Cell(0, 0)
    assert (cell.set_fixed_value(2) is True)
    assert (cell.value_set == {2})


def test_set_fixed_value_failed():
    cell = Cell(0, 0)
    assert (cell.set_fixed_value(2) is True)
    assert (cell.set_fixed_value(2) is False)
    assert (cell.set_fixed_value(6) is False)


def test_eliminate_success():
    cell = Cell(0, 0)
    assert (cell.eliminate(9) is True)
    assert (cell.eliminate(1) is True)


def test_eliminate_failed():
    cell = Cell(0, 0)
    assert (cell.eliminate(9) is True)
    assert (cell.eliminate(9) is False)
