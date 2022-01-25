from timeit import default_timer as timer

import numpy as np

from src.aco.ACOSolver import ACOSolver
from src.genetic_algorithm.GASolver import GASolver


# random.seed(10)

def mainACO(rng):
    solver = ACOSolver(
            random_generator=rng,
            board_size=9,
            board_file="../resources/boards/logic-solvable/hard/aiescargot.txt",
            num_ants=10,
            max_iterations=1000,
            greediness=0.9,
            pheromone_decay=0.1,
            evaporation_rate=0.9,
            best_evaporation_rate=0.005,
            )
    solver.solve()
    print(f"Solved in: {solver.solution_time:.3f}s")
    print(f"Is solution correct: {solver.best_board.is_correct()}")
    print(solver.best_board)


def mainGA():
    solver = GASolver(
        board_path="../resources/ga_boards/easy/board1.txt",
        population_size=21,
        number_generations=1000,
        sudoku_shape=9,
        mutation_probability=0.6,
        elite_param=1,
        tournament_size=5,
        cross_probability=0.4,
        cataclystic_ratio=10000
    )
    solver.initialize_population()
    solver.init_auxiliary()
    start = timer()
    winner = solver.solve()
    end = timer()
    print("~"*10)
    print("Board:")
    print(winner)
    print(f"Solution took {end-start} seconds!")
    solver.show_statistics()


if __name__ == '__main__':
    # Initialise a random number generator
    rng = np.random.default_rng(42)
    mainACO(rng)
    # mainGA()
