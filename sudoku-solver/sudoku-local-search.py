""" This is a Sudoku solver.

Solving Sudoku is problem 1632 on LeetCode
https://leetcode.com/problems/sudoku-solver/

The code below implements a local search algorithm, by populating
each box in the sudoku via a random permutation of allowed values
and repeatedly swapping values to reduce the number of row and column conflicts.
If the number of conflicts does not improve after awhile, we restart.

For more details, see the README in the file's github folder.
"""

from typing import List
import random
from itertools import product

MAX_ATTEMPTS = 1000
RESTART_RATIO = 3
N_h = 3
N_v = 3
N = N_h * N_v
ALPHABET = [str(n) for n in range(1, N+1)]
alphabet_dict = {ALPHABET[i]: i for i in range(N)}
BYE_SYMBOL = '.'


class SetList(object): # a set with random choice
    def __init__(self):
        self.item_to_position = {}
        self.items = []

    def add(self, item):
        if item in self.item_to_position:
            return
        self.items.append(item)
        self.item_to_position[item] = len(self.items)-1

    def remove(self, item):
        position = self.item_to_position.pop(item)
        last_item = self.items.pop()
        if position != len(self.items):
            self.items[position] = last_item
            self.item_to_position[last_item] = position

    def choose_random(self):
        return random.choice(self.items)

    def pop(self):
        item = self.choose_random()
        self.remove(item)
        return item

    def __contains__(self, item):
        return item in self.item_to_position

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return repr(self.items)


class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        # Initialization
        solution=[[None for _ in range(N)] for _ in range(N)]
        row_allowed_values = [{v for v in range(N)} for _ in range(N)]
        column_allowed_values = [{v for v in range(N)} for _ in range(N)]
        box_allowed_values = [{v for v in range(N)} for _ in range(N)]
        row_val_cells = [[set() for _ in range(N)] for _ in range(N)]
        column_val_cells = [[set() for _ in range(N)] for _ in range(N)]
        box_val_cells = [[None for _ in range(N)] for _ in range(N)]

        # Utility functions.
        def box_number(x, y):
            return N_v * (x // N_v) + (y // N_h)

        def is_row_conflicted(x, v):
            return len(row_val_cells[x][v]) > 1

        def is_column_conflicted(y, v):
            return len(column_val_cells[y][v]) > 1

        def is_conflicted(x, y):
            v = solution[x][y]
            return is_row_conflicted(x,v) or is_column_conflicted(y,v)

        def update_conflicted(cells):
            for x, y in cells:
                if is_conflicted(x, y):
                    conflicted.add((x, y))
                else:
                    if (x, y) in conflicted:
                        conflicted.remove((x, y))

        def swap_conflicted_update(x_1, y_1, v_1, x_2, y_2, v_2):
            for x, y, v in product((x_1, x_2), (y_1, y_2), (v_1, v_2)):
                update_conflicted(row_val_cells[x][v])
                update_conflicted(column_val_cells[y][v])

        # Collect forbidden values and copy to solution.
        for i in range(N):
            for j in range(N):
                if board[i][j] != BYE_SYMBOL:
                    val = alphabet_dict[board[i][j]]
                    row_allowed_values[i].remove(val)
                    column_allowed_values[j].remove(val)
                    box_allowed_values[box_number(i, j)].remove(val)
                    solution[i][j] = val

        # Randomly fill each box and build tables to track where everything is.
        def preprocess():
            for box_num in range(N):
                # Get values.
                allowed_values = list(box_allowed_values[box_num])
                random.shuffle(allowed_values)

                corner_i, corner_j = N_v * (box_num // N_v), N_h * (box_num % N_v)
                for di in range(N_v):
                    for dj in range(N_h):
                        i, j = corner_i+di, corner_j+dj
                        # Fill the box.
                        if board[i][j] == BYE_SYMBOL:
                            v = allowed_values.pop()
                            solution[i][j] = v
                        else:
                            v = solution[i][j]

                        # Track cells with value v in each row, column and box.
                        row_val_cells[i][v].add((i, j))
                        column_val_cells[j][v].add((i, j))
                        box_val_cells[box_num][v] = (i, j)  # always one per box

            conflicted_cells = SetList()
            for i in range(N):
                for j in range(N):
                    if is_conflicted(i, j):
                        conflicted_cells.add((i, j))

            number_conflicted_cells = len(conflicted_cells)
            print(f'number of conflicted cells={number_conflicted_cells}')

            return solution, conflicted_cells, number_conflicted_cells, \
                   box_val_cells, row_val_cells, column_val_cells

        solution, conflicted, number_conflicted, \
            box_val_cells, row_val_cells, column_val_cells = preprocess()

        attempt_number = 1
        step = 1
        total_step = 1
        improvement_step = 1
        while attempt_number < MAX_ATTEMPTS:

            if not conflicted: # Victory lap.
                print(f'Solved! in {attempt_number} attempts, in {step} steps, '
                      f'{total_step+step} total, '
                      f'last ratio {step/improvement_step}.')
                for i, row in enumerate(board):
                    for j, val in enumerate(row):
                        board[i][j] = ALPHABET[solution[i][j]]
                break

            step += 1
            if step > improvement_step*RESTART_RATIO and len(conflicted) < 10:
                # Restart.
                attempt_number += 1
                print(f'Restart after {step} steps!'
                      f' (Last improvement at {improvement_step}). '
                      f'Attempt number {attempt_number}.')
                solution, conflicted, number_conflicted, \
                box_val_cells, row_val_cells, column_val_cells = preprocess()

                total_step += step
                step = 1

            # Swap values to try to reduce conflict.

            # Pick a conflicted cell.
            while True:
                i, j = conflicted.choose_random()
                if board[i][j] == BYE_SYMBOL:
                    break
            cell = (i,j)
            val = solution[i][j]
            box_num = box_number(i, j)

            # Choose the swap myopically.
            min_conflict = 4*N
            for alt_val in box_allowed_values[box_num]:
                if alt_val != val:
                    alt_i, alt_j = alt_cell = box_val_cells[box_num][alt_val]
                    conflict = len(row_val_cells[i][alt_val]) +\
                               len(column_val_cells[j][alt_val]) +\
                               len(row_val_cells[alt_i][val]) +\
                               len(column_val_cells[alt_j][val])
                    if conflict < min_conflict:
                        min_conflict = conflict
                        new_i, new_j = new_cell = alt_cell
                        new_val = alt_val

            # Now swap and update including update conflicted.
            # Remove.
            row_val_cells[new_i][new_val].remove(new_cell)
            column_val_cells[new_j][new_val].remove(new_cell)
            row_val_cells[i][val].remove(cell)
            column_val_cells[j][val].remove(cell)

            # Swap.
            new_val, val = val, new_val
            solution[i][j] = val
            solution[new_i][new_j] = new_val

            # Add.
            row_val_cells[new_i][new_val].add(new_cell)
            column_val_cells[new_j][new_val].add(new_cell)
            row_val_cells[i][val].add(cell)
            column_val_cells[j][val].add(cell)

            box_val_cells[box_num][val] = cell
            box_val_cells[box_num][new_val] = new_cell

            swap_conflicted_update(x_1=i, y_1=j, v_1=val,
                                   x_2=new_i, y_2=new_j, v_2=new_val)

            if len(conflicted) < number_conflicted:
                number_conflicted = len(conflicted)
                if number_conflicted > 0:
                    improvement_step = step
                if number_conflicted < 10:
                    print(f'Step {step}, attempt {attempt_number}.')
                    print(f'Number of conflicted cells={number_conflicted}')
                    print(f'Conflicted cells: {conflicted}')


def main():
    board_1 = [
            [".",".",".",".",".",".",".","1","."],
            [".",".",".",".",".","2",".",".","3"],
            [".",".",".","4",".",".",".",".","."],
            [".",".",".",".",".",".","5",".","."],
            ["4",".","1","6",".",".",".",".","."],
            [".",".","7","1",".",".",".",".","."],
            [".","5",".",".",".",".","2",".","."],
            [".",".",".",".","8",".",".","4","."],
            [".","3",".","9","1",".",".",".","."]
            ]
    board_2 = [
        [".",".",".",".","5","."],
        [".","2",".","4",".","6"],
        [".",".","6",".",".","4"],
        [".",".",".",".",".","."],
        ["6",".",".","1",".","."],
        [".","4","3",".",".","."]
        ]

    board_3 = [[".",".",".","2",".",".",".","6","3"],
               ["3",".",".",".",".","5","4",".","1"],
               [".",".","1",".",".","3","9","8","."],
               [".",".",".",".",".",".",".","9","."],
               [".",".",".","5","3","8",".",".","."],
               [".","3",".",".",".",".",".",".","."],
               [".","2","6","3",".",".","5",".","."],
               ["5",".","3","7",".",".",".",".","8"],
               ["4","7",".",".",".","1",".",".","."]]

    file_name = 'test-instances/s08a.txt'
    board_4 = []
    with open(file_name) as f:
        for line in f.read().splitlines():
            if line:
                raw_row = line.split(' ')[:-1]
                row = [BYE_SYMBOL if x == '0' else x for x in raw_row]
                board_4.append(row)

    board = board_3
    sol = Solution()
    sol.solveSudoku(board)
    for row in board:
        print(row)


if __name__ == '__main__':
    main()
