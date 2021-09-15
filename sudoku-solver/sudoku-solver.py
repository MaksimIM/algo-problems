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
from typing import List

N_h = 3
N_v = 3
N = N_h * N_v
ALPHABET = [str(n) for n in range(1, N+1)]
BYE_SYMBOL = '.'


class Cell:
    def __init__(self, i, j, possible_values=None, neighbours=None):
        self._i = i
        self._j = j

        if possible_values is None:
            self.possible_values = set(ALPHABET)
        else:
            self.possible_values = possible_values
        if neighbours is None:
            self.neighbours = set()
        else:
            self.neighbours = neighbours

    @property
    def i(self):
        return self._i

    @property
    def j(self):
        return self._j

    def ordered_possible_values(self):
        if len(self.possible_values) < 2:
            return self.possible_values
        return sorted(self.possible_values, key=self._how_constraining)

    def _how_constraining(self, value):
        return [(value in nbr.possible_values)
                for nbr in self.neighbours].count(True)


def _all_neighbors(i, j):
    """Returns indexes of all entries neighboring (i,j) in the sudoku board"""
    neighbours = [(i, c) for c in range(N)] + [(r, j) for r in range(N)]
    k_0, l_0 = N_h * (i // N_h), N_v * (j // N_v)
    for dk in range(N_h):
        for dl in range(N_v):
            neighbours += [(k_0 + dk, l_0 + dl)]
    return neighbours


def _allowed_values(i, j, board_list):
    """Returns all values that the entry (i,j) may be given
    without violating the sudoku constraints."""
    forbidden_values = {board_list[k][l] for k, l in _all_neighbors(i, j)}
    return {x for x in ALPHABET if x not in forbidden_values}


class Sudoku:
    def __init__(self, board_list):
        self._board = board_list
        self._unfilled = self._build_que()

    @property
    def board(self):
        return self._board

    def _build_que(self):
        table = self._table_of_cells()
        # Processes the table of cells into a queue of cells.
        board_que = [set() for _ in range(N + 1)]
        for i in range(N):
            for j in range(N):
                cell = table[i][j]
                if cell:
                    board_que[len(cell.possible_values)].add(cell)
        return board_que

    def _table_of_cells(self):
        """Make a table of cell objects from the board"""
        table = [[None for _ in range(N)] for _ in range(N)]
        for i in range(N):
            for j in range(N):
                if self._board[i][j] == BYE_SYMBOL:
                    table[i][j] = Cell(i, j, _allowed_values(i, j, self._board))
        # Set the neighbors of the cell objects.
        for i in range(N):
            for j in range(N):
                if table[i][j]:
                    table[i][j].neighbours = {table[k][l]
                                              for (k, l) in _all_neighbors(i, j)
                                              if ((k, l) != (i, j)
                                              and table[k][l])}
        return table

    def _fill_cell_neighbours(self, current_cell, tentative_value):
        """Restrict possible values of neighbors.
        Record which neighbors are affected for backtracking.
        Return the set of affected neighbours."""
        modified_neighbours = set()
        for nbr in current_cell.neighbours:
            if tentative_value in nbr.possible_values:
                modified_neighbours.add(nbr)
                self._unfilled[len(nbr.possible_values)].remove(nbr)
                nbr.possible_values.remove(tentative_value)
                self._unfilled[len(nbr.possible_values)].add(nbr)
        return modified_neighbours

    def _unfill_cell_neighbours(self, tentative_value, modified_neighbours):
        for neighbour in modified_neighbours:
            self._unfilled[len(neighbour.possible_values)].remove(neighbour)
            neighbour.possible_values.add(tentative_value)
            self._unfilled[len(neighbour.possible_values)].add(neighbour)

    def solve(self):
        """Check if done and find a most constrained cell otherwise."""
        if self._unfilled[0]:
            return False
        d = 1
        while not self._unfilled[d]:
            d += 1
            if d == N + 1:
                return True
        current_cell = self._unfilled[d].pop()

        # Prepare for the recursion.
        for neighbour in current_cell.neighbours:
            neighbour.neighbours.remove(current_cell)

        '''Iterate over possible values trying to fill with them.'''
        for tentative_value in current_cell.possible_values:
            # Alternatively, iterate over current_cell.ordered_possible_values()
            # to use the "least constraining" heuristic.
            modified_neighbours = self._fill_cell_neighbours(current_cell,
                                                             tentative_value)

            # See if smaller sudoku is solved. If not, undo the changes.
            if self.solve():
                self.board[current_cell.i][current_cell.j] = tentative_value
                return True
            else:
                self._unfill_cell_neighbours(tentative_value,
                                             modified_neighbours)

        # All values failed. This means we should've chosen a different value
        # for one of the previous cells. We now undo the changes to the
        # priority queue, to restore state for backtracking.
        self._unfilled[d].add(current_cell)
        for neighbour in current_cell.neighbours:
            neighbour.neighbours.add(current_cell)


class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """The main solving method."""
        the_sudoku = Sudoku(board)
        the_sudoku.solve()
        # Problem specification expects variable 'board'
        # to contain the solved sudoku.
        board = the_sudoku.board


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


    file_name='test-instances/s09a.txt'
    board_3 = []
    with open(file_name) as f:
        for line in f.read().splitlines():
            if line:
                raw_row=line.split(' ')[:-1]
                row=[BYE_SYMBOL if x=='0' else x for x in raw_row]
                board_3.append(row)

    board = board_3

    sol = Solution()
    sol.solveSudoku(board)
    for row in board:
        print(row)


if __name__ == '__main__':
    main()
