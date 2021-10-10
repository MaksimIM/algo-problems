## Word Search (II)

This is a solution for the Word Search II, problem 212 on LeetCode:

https://leetcode.com/problems/word-search-ii/

### The problem.

Given an `m x n` board of characters and a list of strings `words`,
return all words on the board.

Each word must be constructed from letters of sequentially 
adjacent cells, where adjacent cells are horizontally or 
vertically neighboring. The same letter cell may not be used 
more than once in a word.


### A solution.

We put all words into a [trie](https://en.wikipedia.org/wiki/Trie). 
Starting from each cell we explore all neighbors that may lead to a word
(as determined by the trie), recursively. 

### Some optimizations.

We delete any found word from the trie 
(on LeetCode testcases this gives about a 20-fold speed-up).

Since we repeatedly look up cell's neighbors, and the table is small,
we build a dictionary of all the cells 
(this gives a 10 to 20 percent speedup).


