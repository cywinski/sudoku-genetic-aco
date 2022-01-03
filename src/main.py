import time

from src.aco.ACOSolver import ACOSolver


def main():
    start = time.time()
    solver = ACOSolver(
            board_size=9,
            board_file="../resources/boards/logic-solvable/goldennugget.txt",
            num_ants=10,
            max_iterations=0,
            greediness=0.9,
            pheromone_decay=0.1,
            evaporation_rate=0.9,
            best_evaporation_rate=0.005
            )
    result = solver.solve()
    end = time.time()
    print(f"Solved in: {end - start:.3f}s")
    print(f"Is solution correct: {result.board.is_correct()}")
    print(result.board)


if __name__ == '__main__':
    main()
