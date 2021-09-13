## Rank Transform of a Matrix

This is a solution for the Rank Transform of a Matrix problem, problem 1632 on LeetCode:

https://leetcode.com/problems/rank-transform-of-a-matrix/

### The problem

The problem asks that given an `nxm` matrix we compute a new matrix of **ranks**, 
where the rank of a cell in out matrix is an integer that represents how large an element in that cell is compared to other elements. It is calculated using the following rules:

* Each `rank` is a positive integer.

* If two elements p and q are in the same row or column, then:
  * If `p < q` then `rank(p) < rank(q)`
  * If `p == q` then `rank(p) == rank(q)`
  
* The rank is as small as possible under these conditions.

The last condition may seem ambiguous.  However, suppose we fix a given starting matrix.
Then among all the functions `r` satisfying the first two conditions there exists one - which we will call `rank` - such that `rank(p) <= r(p)` for all other `r` and all `p`. This makes `rank` unambiguously 'as small as possible under these conditions', and this is the one that we should compute. In fact, existence of such 'minimal' `rank` function will follow from the solution.  

### The solution

The basic idea is simple:
going from lowest values to highest,
for a given value, find groups of cells with that value
that must have the same rank.
For a given group, that rank must be
one more than the maximum of ranks already assigned
to cells in the rows and columns of the group.
Thus, we assign this rank to all cells in the group,
do this for all groups and then move on to the next value.

A **key optimization** is to find the groups of cells of same rank
not by looking for connected components of the  graph whose vertices
are cells, but, rather, in a graph whose vertices are (row or column)
indexes. For a fixed value `v`, a vertex in this graph is any index such
that in the corresponding row or column there is a cell with value `v`.
This cell is then an edge between its row index and its column index.
All such cells that are edges in a connected component
of our graph need to be assigned their rank simultaneously.

It is important that for each `v` we initialize the graph
to have only the vertices (indexes) that actually contain cells with value `v`.
Then the number of vertices will be at most twice the number of edges (which is not necessarily the case for graphs that contain vertices of degree zero),
and the component search will take `O(V+E)=O(E)` for each value, if done via
a BFS or a DFS graph exploration algorithm.
Summing over all values `v`, we see that finding components
is will take time linear in the number of cells involved, `C`.

An alternative to component finding via BFS/DFS is an implementation that uses a union-find data structure instead.
When fully optimized, it performs component-finding in `O(C alpha(C))` time.
Here `alpha` is the inverse Ackermann function,
which is at most 4 for all practical input sizes
(an `n` for which `alpha(n)>4` would require more bits to write down
than there are atoms in the universe; you can read about all of this [on Wikipedia](https://en.wikipedia.org/wiki/Disjoint-set_data_structure), or see the full derivation in Week 2 of Stanford's [Greedy Algorithms, Minimum Spanning Trees, and Dynamic Programming](https://www.coursera.org/learn/algorithms-greedy) course). 

I provide both implementations via EdgesToComponentsBFS and EdgesToComponentsUF
classes, which inherit from abstract EdgesToComponentsBase and provide their own
implementations of the generate_components method. Furthermore, I implement
both size-based and rank-based union strategies for the union-find version (see any of the references above for what this means).

The time performance of all three versions on LeetCode test cases are not too different,
(the BFS version is a bit faster, landing in 99th percentile on LeetCode).
The union-find version uses less memory,
because it does not need to maintain neighbor-dictionary versions of the graphs.


Overall, the worst-case complexity of each implementation is `O(C ln C)`,
due to the sorting of the matrix values.
After that step the rest runs in
`O(C)` (BFS)/`O(C alpha(C))` (rank-based UF)/`O(C ln(C))` (size-based UF)
time.

## Some final notes:

0) To have a fast rank-assignment method, we maintain a lookup table of
currently maximal ranks in each row/column. The rank of a component is then
one more than the maximal rank already present.
1) In the union-find version, to maintain sub-cubic (in N) complexity
one needs at least one optimization in component finding,
either merge-by-size or merge by rank, to ensure logarithmic time
for find and union operations. To obtain the `O(C alpha(C))` complexity,
union by rank with path compression is needed. In practice,
path compression makes little difference on the LeetCode examples.
2) There are some alternative approaches to implementing the BFS version.
For example, instead of the sets of edges, one could directly build
two dictionaries, one mapping a value to all the indexes relevant to that value
(aka the vertices of the corresponding graph) and one mapping and index-vertex
(and a value) to all its neighbors. This has similar performance but would make
the BFS/DFS implementation diverge more from the union-find one. So we stick to
the "dictionary of edges" version (and generate neighbours when needed)
