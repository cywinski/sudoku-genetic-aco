from src.aco.ACOSolver import ACOSolver


def main():
    solver = ACOSolver(
        board_size=9,
        board_file="../resources/boards/board1.txt",
        num_ants=10,
        max_iterations=10,
        greediness=0.4
    )
    result = solver.solve()
    print(result.board)


if __name__ == '__main__':
    main()
