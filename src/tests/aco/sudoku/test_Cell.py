from src.aco.sudoku.Cell import Cell


def test_create_cell():
    cell = Cell(0, 0)

    assert (cell.x == 0)
    assert (cell.y == 0)
    assert (cell.value_set == {1, 2, 3, 4, 5, 6, 7, 8, 9})


def test_set_fixed_value_success():
    cell = Cell(0, 0)
    cell.set_fixed_value(2)
    assert (cell.value_set == {2})


def test_eliminate_success():
    cell = Cell(0, 0)
    cell.eliminate(9)
    assert (9 not in cell.value_set)
