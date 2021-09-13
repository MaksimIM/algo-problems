## A Sudoku solver

This is a solution for the Solving Sudoku problem, problem 1632 on LeetCode

https://leetcode.com/problems/sudoku-solver/

### The problem

Write a program to solve a Sudoku puzzle by filling the empty cells.

A sudoku solution must satisfy all of the following rules:

* Each of the digits `1-9` must occur exactly once in each row.
* Each of the digits `1-9` must occur exactly once in each column.
* Each of the digits `1-9` must occur exactly once in each of the 9 3x3 sub-boxes of the grid.
The `'.'` character indicates empty cells.

### A solution

The code is suitable for solving `N x N` case with arbitrary alphabet of symbols of length `N^2`, the usual case corresponding to `N=3` and the alphabet `('1', '2', '3', '4', '5', '6', '7', '8', '9')`. It is easy to adapt to the general `M x N` case as well.

This problem is an instance of **constraint satsfaction problem**. The code implements a backtracking algorithm with the
"most constrained first" also known as **minimal remaing values** heuristic for choosing which cell to fill. For a discussion of all this and more see  Chapter 6 of Russel and Norvig's [Artificial Intelligence: A Modern Approach](http://aima.cs.berkeley.edu/contents.html).

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
However, it did not improve performance, and so is disabled in the code. An alternative approach via Local Search is not implemented here.
