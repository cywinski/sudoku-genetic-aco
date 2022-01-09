import numpy as np

from src.aco.ACOSolver import ACOSolver
from src.aco.Ant import Ant

TEST_ACO_SOLVER = ACOSolver(
    board_size=9,
    board_file="../../../resources/boards/board1.txt",
    num_ants=10,
    max_iterations=100,
    greediness=0.4
)


def test_init_global_pheromone():
    expected_result = np.array([[1 / (9 ** 2)] * 9] * (9 ** 2))

    assert (TEST_ACO_SOLVER.global_pheromone.shape == (81, 9))
    assert (np.array_equal(TEST_ACO_SOLVER.global_pheromone, expected_result))


def test_init_ants():
    ants = TEST_ACO_SOLVER._init_ants()
    assert (len(ants) == TEST_ACO_SOLVER.num_ants)
    assert (all(isinstance(ant, Ant) for ant in ants))
    assert (len(set([ant.pos for ant in ants])) == TEST_ACO_SOLVER.num_ants)
