import math
import os
import copy
import random
from typing import List


def is_ok_mini_board(current: List, original: List):
    for el_curr, el_orig in zip(current, original):
        if el_curr == 0:
            raise Exception("New mini board should not contain zeros!")
        if el_orig != 0 and el_curr != el_orig:
            return False
    return True


class Individual:
    def __init__(self, sudoku_shape: int = 9):
        self.sudoku_shape = sudoku_shape
        self.board = []
        self.rating = None

    def init_from_file(self, path: str):
        if not os.path.isfile(path):
            return False
        self.board.clear()
        sudoku_file = []
        with open(path, "r") as rf:
            for line in rf:
                sudoku_row = line.rstrip()
                for num in sudoku_row:
                    sudoku_file.append(num)

        for mini_board_index in range(self.sudoku_shape):
            mini_board = []
            mini_board_shape = int(math.sqrt(self.sudoku_shape))
            for row in range(mini_board_shape):
                for column in range(mini_board_shape):
                    mini_board.append(int(
                        sudoku_file[int(mini_board_index / mini_board_shape) * mini_board_shape * self.sudoku_shape +
                                    mini_board_index % mini_board_shape * mini_board_shape + row * self.sudoku_shape +
                                    column]))
            self.board.append(mini_board)
        return True

    def create_with_shuffle(self):
        if len(self.board) == 0:
            return False
        for ind_mini_board in range(len(self.board)):
            numbers_to_fill = []
            for number in range(1, self.sudoku_shape + 1):
                if number not in self.board[ind_mini_board]:
                    numbers_to_fill.append(number)
            random.shuffle(numbers_to_fill)
            for ind_number in range(len(self.board[ind_mini_board])):
                if self.board[ind_mini_board][ind_number] == 0:
                    self.board[ind_mini_board][ind_number] = numbers_to_fill.pop()
        return True

    def is_board_ok_in_mini_boards(self):
        ok_board = [x for x in range(1, self.sudoku_shape + 1)]
        board_copy = copy.deepcopy(self.board)
        for mini_board in board_copy:
            if 0 in mini_board:
                raise Exception("Function is_board_ok_in_mini_boards executed with zeros!")
            sorted_board = copy.deepcopy(mini_board)
            sorted_board.sort()
            if sorted_board != ok_board:
                return False
        return True

    def mutate(self, comparator: List[List], mutation_probability: float = 0.5):
        # MAYBE ONLY ONE MUTATION IS NOT ENOUGH
        for index_mini_board in range(len(self.board)):
            if random.random() < mutation_probability:
                positions = [x for x in range(0, self.sudoku_shape)]
                mutated_positions = random.sample(population=positions, k=2)
                new_board = copy.deepcopy(self.board[index_mini_board])
                new_board[mutated_positions[0]] = self.board[index_mini_board][mutated_positions[1]]
                new_board[mutated_positions[1]] = self.board[index_mini_board][mutated_positions[0]]
                if is_ok_mini_board(new_board, comparator[index_mini_board]):
                    self.board[index_mini_board] = new_board

    def rate(self):
        if self.is_board_ok_in_mini_boards() is False:
            raise Exception("Something went wrong and some mini_board is invalid!")
        rating = 0
        ok_permutation = [x for x in range(1, self.sudoku_shape + 1)]
        mini_board_shape = int(math.sqrt(self.sudoku_shape))
        # count for each row
        for row in range(self.sudoku_shape):
            collect_row = []
            for mini_board_index in range(int(row / mini_board_shape) * mini_board_shape,
                                          int(row / mini_board_shape) * mini_board_shape + mini_board_shape):
                for index_in_mini_board in range(mini_board_shape):
                    collect_row.append(
                        self.board[mini_board_index][(row % mini_board_shape) * mini_board_shape + index_in_mini_board])
            for ok_number in ok_permutation:
                if ok_number not in collect_row:
                    rating += 1
        # count for each column
        for column in range(self.sudoku_shape):
            collect_column = []
            for mini_board_index in range(int(column / mini_board_shape), self.sudoku_shape, mini_board_shape):
                for index_in_mini_board in range(column % mini_board_shape, self.sudoku_shape, mini_board_shape):
                    collect_column.append(self.board[mini_board_index][index_in_mini_board])
            for ok_number in ok_permutation:
                if ok_number not in collect_column:
                    rating += 1
        # if rating is repeating, add penalty

        # if self.actual_rating is None or self.actual_rating != rating:
        #     self.actual_rating = rating
        #     self.rating = rating
        #     self.n_of_repeated_ratings = 0
        # elif rating == self.actual_rating:
        #     self.n_of_repeated_ratings += 1
        #     self.rating += 1

        self.rating = rating
