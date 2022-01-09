from src.aco.ACOSolver import ACOSolver


def main():
    solver = ACOSolver(
        board_size=9,
        board_file="../resources/boards/platiniumblonde.txt",
        num_ants=10,
        max_iterations=100,
        greediness=0.9,
        pheromone_decay=0.1,
        evaporation_rate=0.9,
        best_evaporation_rate=0.005
    )
    result = solver.solve()
    print(result.board)


if __name__ == '__main__':
    main()
