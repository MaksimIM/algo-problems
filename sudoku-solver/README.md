## Two Sudoku solvers

This repo contains two solutions for the Solving Sudoku problem, problem 1632 on LeetCode

https://leetcode.com/problems/sudoku-solver/

### The problem

Write a program to solve a Sudoku puzzle by filling the empty cells.

A sudoku solution must satisfy all of the following rules:

* Each of the digits `1-9` must occur exactly once in each row.
* Each of the digits `1-9` must occur exactly once in each column.
* Each of the digits `1-9` must occur exactly once in each of the 9 3x3 sub-boxes of the grid.
The `'.'` character indicates empty cells.

### Discussion of solutions

Both versions of the code are suitable for solving any `N x N` sudoku 
with `N` boxes of size   `N = N_h x N_v` with arbitrary alphabet of symbols 
of length `N`, the usual case corresponding to `N_h=N_v=3` and the alphabet
`('1', '2', '3', '4', '5', '6', '7', '8', '9')`. 

This problem is an instance of **constraint satisfaction problem**. 
For a discussion of such problems, see  Chapter 6 of Russel and Norvig's 
[Artificial Intelligence: A Modern Approach](http://aima.cs.berkeley.edu/contents.html).
It covers the general ideas that are behind both of the algorithms presented here.

Both scripts can be run on LeetCode and locally. The local versions uses some of the benchmark sudoku instances found on the [Sudoku research page](http://lipas.uwasa.fi/~timan/sudoku/)
from University of Vaas. These can be found in the test-instances folder of this repo.


#### The main approach
The main approach implements a backtracking algorithm with the
"most constrained first" also known as **minimal remaining values** heuristic for choosing which cell to fill. 

Specifically, we maintain the board as **a priority queue of cells**,
ordered by number of possible values that can be put into that cell
without violating the sudoku constraints.
(The abstract data type of [priority queue](https://en.wikipedia.org/wiki/Priority_queue) is **implemented as an array of sets of cells**,
with index being the number of possible values.
This is an efficient implementation for our use case,
since our priorities only take values between 0 and 10.)
We then try to fill in one of the most constrained cells,
update the priority queue, and recurse.

The number of operations required to fill a cell
depends on the number of its unfilled neighbours.
In the worst cases, this is `O(N^2)` (where `N=3` for usual Sudoku).
Hence the overall running time is `O(N^2 x number of cell-fillings)`.
(This is in contrast to `O(N^3 x number of cell-fillings)` for the queue-less
version that computes a least-constrained cell "on the fly", or
`O(N^2 log N x number of cell-fillings)` for a heap-based queue version).
In practice the code runs fairly quickly
(36 to 51 ms on LeetCode, 99th to 95th percentile
and under 2 seconds on the following challenging test case:
```
[
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
```
).

I have also implemented the "least constraining value first"
for choosing which values to try.
However, it did not improve performance, and so is disabled in the code.

#### An alternative approach

An alternative approach is via **local search**. It operates by filling in each box
using a random permutation of allowed values 
(that is, we exclude the values of the pre-filled cells and permute the rest, 
filling the whole box). This creates conflicts wherever the 
same value appears several times in some row or column.
We call the cells where such troublesome values are located 'conflicted'. 
We then repeatedly swap a random conflicted cell with one of its box-mates, 
attempting to reduce the amount of conflict. This is a "local" move, in the 
sense of trying to improve the filling by small changes. Of course, such local 
optimizers can get stuck in local minima.  There is a small amount of resistance
to this, since, once one of the conflicted cells is picked, we force a swap 
even if it would increase the amount of conflict. This allows us to perturb
away from a local minimum. However, this is sometimes insufficient. As a 
fail-safe, we simply restart after we fail to see an improvement for a while
(how long we wait is controlled by the "restart ratio" parameter, which is the minimal
ratio (number of steps so far)/(the number of steps from start till last improvement)
which triggers a restart).

For most sudoku instances this method is not as efficient as our main approach,
but it still passes the LeetCode tester once in a while (about 20% of time).
 
