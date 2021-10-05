""" This is a Sudoku solver.

Solving Sudoku is problem 1632 on LeetCode

https://leetcode.com/problems/sudoku-solver/

The code below implements a backtracking algorithm with the
"most constrained first" heuristic for choosing which cell to fill.

It  maintains the board as a priority queue of cells,
ordered by number of possible values that can be put into that cell
without violating the sudoku constraints.
We  try to fill in one of the most constrained cells,
update the priority queue, and recurse.

For more details, see the README in the file's github folder.
"""
from __future__ import annotations
from sys import stdout
import dataclasses
from itertools import product

HORIZONTAL_SIZE = 3
VERTICAL_SIZE = 3
SIZE = HORIZONTAL_SIZE * VERTICAL_SIZE
ALPHABET = tuple(map(str, range(1, SIZE+1)))
EMPTY_SYMBOL = '.'


@dataclasses.dataclass(unsafe_hash=True)
class Cell:
    x_pos: int
    y_pos: int
    possible_values: set[str] = dataclasses.field(compare=False, repr=False)
    neighbours: set[Cell] = dataclasses.field(init=False, compare=False, repr=False)

    def ordered_possible_values(self):
        def how_constraining(value):
            return sum(
                value in neighbour.possible_values
                for neighbour in self.neighbours
            )
        return sorted(self.possible_values, key=how_constraining)


def neighbour_positions(x_pos, y_pos):
    for neighbor_y in range(SIZE):
        yield x_pos, neighbor_y
    for neighbor_x in range(SIZE):
        yield neighbor_x, y_pos
    top_left_x = (x_pos // HORIZONTAL_SIZE) * HORIZONTAL_SIZE
    top_left_y = (y_pos // VERTICAL_SIZE) * VERTICAL_SIZE
    for delta_x in range(HORIZONTAL_SIZE):
        for delta_y in range(VERTICAL_SIZE):
            yield top_left_x + delta_x, top_left_y + delta_y


def allowed_values(x_pos, y_pos, board):
    """Returns all values that the entry (x_pos,y_pos) may be given
    without violating the sudoku constraints."""
    forbidden_values = {board[k][l] for k, l in neighbour_positions(x_pos, y_pos)}
    return set(ALPHABET) - forbidden_values


def build_que(board):
    table = table_of_cells(board)
    # Processes the table of cells into a queue of cells.
    board_que = [set() for _ in range(SIZE + 1)]
    for x_pos, y_pos in product(range(SIZE), range(SIZE)):
        cell = table[x_pos][y_pos]
        if cell is None:
            continue
        board_que[len(cell.possible_values)].add(cell)
    return board_que


def table_of_cells(board):
    """Make a table of cell objects from the board"""
    table = [[None for _ in range(SIZE)] for _ in range(SIZE)]

    for x_pos, y_pos in product(range(SIZE), range(SIZE)):
        if board[x_pos][y_pos] != EMPTY_SYMBOL:
            continue
        table[x_pos][y_pos] = Cell(x_pos, y_pos,
                                   allowed_values(x_pos, y_pos, board))
    # Set the neighbors of the cell objects.
    for x_pos, y_pos in product(range(SIZE), range(SIZE)):
        if table[x_pos][y_pos] is None:
            continue
        table[x_pos][y_pos].neighbours = {table[k][l]
                                          for (k, l) in neighbour_positions(x_pos, y_pos)
                                          if ((k, l) != (x_pos, y_pos)
                                          and table[k][l] is not None)}
    return table


@dataclasses.dataclass()
class Sudoku:
    board: list[list[str]]
    unfilled: list[set[Cell]] = dataclasses.field(init=False)

    def __post_init__(self):
        self.unfilled = build_que(self.board)


def solve(sudoku):
    """Check if done and find a most constrained cell otherwise."""
    if sudoku.unfilled[0]:
        return False
    d = 1
    while not sudoku.unfilled[d]:
        d += 1
        if d == SIZE + 1:
            return True
    current_cell = sudoku.unfilled[d].pop()

    # Prepare for the recursion.
    for neighbour in current_cell.neighbours:
        neighbour.neighbours.remove(current_cell)

    '''Iterate over possible values trying to fill with them.'''
    for tentative_value in current_cell.possible_values:
        # Alternatively, iterate over current_cell.ordered_possible_values()
        # to use the "least constraining" heuristic.
        modified_neighbours = fill_cell_neighbours(sudoku, current_cell,
                                                   tentative_value)

        # See if smaller sudoku is solved. If not, undo the changes.
        if solve(sudoku):
            sudoku.board[current_cell.x_pos][current_cell.y_pos] = tentative_value
            return True
        else:
            unfill_cell_neighbours(sudoku, tentative_value,
                                   modified_neighbours)

    # All values failed. This means we should've chosen a different value
    # for one of the previous cells. We now undo the changes to the
    # priority queue, to restore state for backtracking.
    sudoku.unfilled[d].add(current_cell)
    for neighbour in current_cell.neighbours:
        neighbour.neighbours.add(current_cell)

    # Indicate branch failure.
    return False


def fill_cell_neighbours(sudoku, current_cell, tentative_value):
    """Restrict possible values of neighbors.
    Record which neighbors are affected for backtracking.
    Return the set of affected neighbours."""
    modified_neighbours = set()
    for nbr in current_cell.neighbours:
        if tentative_value in nbr.possible_values:
            modified_neighbours.add(nbr)
            sudoku.unfilled[len(nbr.possible_values)].remove(nbr)
            nbr.possible_values.remove(tentative_value)
            sudoku.unfilled[len(nbr.possible_values)].add(nbr)
    return modified_neighbours


def unfill_cell_neighbours(sudoku, tentative_value, modified_neighbours):
    for neighbour in modified_neighbours:
        sudoku.unfilled[len(neighbour.possible_values)].remove(neighbour)
        neighbour.possible_values.add(tentative_value)
        sudoku.unfilled[len(neighbour.possible_values)].add(neighbour)


def board_from_file(file_in, file_empty_symbol):
    board = []
    for line in file_in.read().splitlines():
        if line:
            raw_row = line.split(' ')[:-1]
            row = [EMPTY_SYMBOL if x == file_empty_symbol else x for x in raw_row]
            board.append(row)
    return board


def solve_files(file_in, file_out, file_empty_symbol):
    board_in = board_from_file(file_in, file_empty_symbol)
    print('Solving')
    for row in board_in:
        print("".join(row))
    print('\n')

    sudoku = Sudoku(board_in)
    consistent = solve(sudoku)
    if not consistent:
        file_out.write('No solution.')
    else:
        file_out.write('Solution: \n\n')
        for row in sudoku.board:
            file_out.write("".join(row) + "\n")


# For LeetCode
class Solution:
    def solveSudoku(self, board: list[list[str]]) -> None:
        """The main solving method."""
        sudoku = Sudoku(board)
        consistent = solve(sudoku)
        if not consistent:
            pass  # Error out
        board = sudoku.board


def main():
    with open("test-instances/s09a.txt") as file_in:
        solve_files(file_in, stdout, '0')


if __name__ == '__main__':
    main()
