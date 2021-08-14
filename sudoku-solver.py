""" We maintain the board as a priority queue of cells,
    ordered by number of possible values that can be put into that cell
    without violating the sudoku constraints.
    (The abstract data type of queue is implemented as an array of sets of cells,
    with index being the number of possible values.
    This is an efficient implementation for our use case,
    since our priorities only take values between 0 and 10.)
    We then try to fill in one of the most constrained cells,
    update the priority queue, and recurse.

    The above implements the "most constrained first" heuristic
    for choosing which cell to fill.
    I have also implemented the "least constraining value first"
    for choosing which values to try.
    However, it did not improve performance, an so is disabled in the code below.
"""
ALPHABET = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
N = 3


class Cell:
    def __init__(self, i, j, possible_values=None, neighbours=None):
        self.i = i
        self.j = j

        if possible_values is None:
            self.possible_values = set(ALPHABET)
        else:
            self.possible_values = possible_values
        if neighbours is None:
            self.neighbours = set()
        else:
            self.neighbours = neighbours

    def ordered_possible_values(self):
        if len(self.possible_values) < 2:
            return self.possible_values
        return sorted(self.possible_values, key=self.how_constraining)

    def how_constraining(self, value):
        return [(value in nbr.possible_values) for nbr in self.neighbours].count(True)


def all_neighbors(i, j):
    """Returns indexes of all entries neighboring (i,j) in the sudoku board"""
    answer = [(i, c) for c in range(N * N)] + [(r, j) for r in range(N * N)]
    k_0, l_0 = N * (i // N), N * (j // N)
    for dk in range(N):
        for dl in range(N):
            answer += [(k_0 + dk, l_0 + dl)]
    return answer


def allowed_values(i, j, board_list):
    """Returns all values that the entry (i,j) may be given
    without violating the sudoku constraints."""
    forbidden_values = {board_list[k][l] for k, l in all_neighbors(i, j)}
    return {x for x in ALPHABET if x not in forbidden_values}


class Sudoku:
    def __init__(self, board_list):
        self._board = board_list
        self._unfilled = self.build_que()

    @property
    def board(self):
        return self._board

    def build_que(self):
        table = self.table_of_cells()
        '''Processes the table of cells into the queue of cells'''
        board_que = [set() for _ in range(N * N + 1)]
        for i in range(N * N):
            for j in range(N * N):
                cell = table[i][j]
                if cell:
                    board_que[len(cell.possible_values)].add(cell)
        return board_que

    def table_of_cells(self):
        """Make a table of cell objects from the board"""
        table = [[None for _ in range(N * N)] for _ in range(N * N)]
        for i in range(N * N):
            for j in range(N * N):
                if self.board[i][j] == '.':
                    table[i][j] = Cell(i, j, allowed_values(i, j, self.board))
        'Set the neighbors of the cell objects.'
        for i in range(N * N):
            for j in range(N * N):
                if table[i][j]:
                    table[i][j].neighbours = {table[k][l] for (k, l) in all_neighbors(i, j) if
                                              ((k, l) != (i, j) and table[k][l])}
        return table

    def fill_cell_nbrs(self, current_cell, tentative_value):
        """Restrict possible values of neighbors.
        Record which neighbors are affected for backtracking."""
        modified_neighbours = set()
        for nbr in current_cell.neighbours:
            if tentative_value in nbr.possible_values:
                modified_neighbours.add(nbr)
                self._unfilled[len(nbr.possible_values)].remove(nbr)
                nbr.possible_values.remove(tentative_value)
                self._unfilled[len(nbr.possible_values)].add(nbr)
        return modified_neighbours

    def unfill_cell_nbrs(self, tentative_value, modified_neighbours):
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
            if d == N * N + 1:
                return True
        current_cell = self._unfilled[d].pop()

        '''Prepare for the recursion.'''
        for neighbour in current_cell.neighbours:
            neighbour.neighbours.remove(current_cell)

        '''Iterate over possible values trying to fill with them.'''
        for tentative_value in current_cell.possible_values:
            # Alternatively, iterate over current_cell.ordered_possible_values()
            # to use the "least constraining" heuristic.
            modified_neighbours = self.fill_cell_nbrs(current_cell, tentative_value)

            '''See if smaller sudoku is solved. If not, undo the changes.'''
            if self.solve():
                self.board[current_cell.i][current_cell.j] = tentative_value
                return True
            else:
                self.unfill_cell_nbrs(tentative_value, modified_neighbours)

        '''Undo the changes to the priority queue, to restore state for backtracking.'''
        self._unfilled[d].add(current_cell)
        for neighbour in current_cell.neighbours:
            neighbour.neighbours.add(current_cell)


class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """The main solving method."""
        the_sudoku = Sudoku(board)
        the_sudoku.solve()
        # Problem specification expects variable 'board' to contain the solved sudoku.
        board = the_sudoku.board
