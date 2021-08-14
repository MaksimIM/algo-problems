"""The basic idea is simple:
going from lowest values to highest,
for a given value, find groups of cells with that value
that must have the same rank.
For a given group, that rank must be
one more than the maximal ranks already assigned
to cells in the rows and columns of the group.
Thus we assign this rank to all cells in the group,
do this for all groups and then move on to the next value.

A key optimization is to find the groups of cells of same rank
not by looking for connected components of the whose vertices
are cells, but rather in a graph whose vertices are (row or column)
indexes. For a given value v, a vertex in this graph is any index such
that in the corresponding row or column there is a cell with value v.
This cell is then an edge between its row index and its column index.

It is important that for each v we initialize the graph
to have only the vertices (indexes) that actually contain cells
with value v, and to have an efficient way of finding neighbours of such an index.
Then the number of vertices will be at most twice the number of edges,
and the component search will take O(V+E)=O(E),
that is will take time linear in the number of cells involved, C.

There are several approaches to this.
We can precompute the dictionaries which allow initializing the graph vertices
and looking up neighbors. This takes O(C) time and then allows O(1) lookups.
Alternatively, we initialize a single dictionary mapping a value to all the cells
in that value. We then, for each value separately, compute vertices
and make a neighbours dictionary for that value's graph. This takes O(C) time upfront,
and O(vertices) extra time for each value.
Both approaches run in O(C) time overall and use O(C) extra memory.
On leetcode testcases, the speeds of the two approaches are essentially the same,
and the second approach uses only marginally less memory.
The second approach is also more similar to an alternative union-find implementation.
Below, the second approach is implemented.


In addition, we maintain a lookup table recording
current maximal rank for every index, so computing
the rank for a group and filling it in will also run in O(C) time.
This means that after initial sorting of the values
(which can take as long as O(ClnC) where C is the number of cells),
the rest of the algorithm runs in O(C) time.

It is possible (and is a popular alternative) to use
union-find data structure to find connected components.
An advantage of that approach is that there is no need
to have a lookup of neighbors, as one just directly iterates
over edges (cells) to build connected components.
However to maintain sub-cubic (in N) complexity:
1) one still needs to initialize with only the relevant vertices
2) one needs at least one optimization in union find based component finding,
either merge-by-size or merge by rank, to ensure logarithmic time
for find and union operations.
We will implement this alternative strategy separately.
"""
from collections import deque
from collections import defaultdict
from typing import List


class Ranker:
    def __init__(self, matrix):
        self.matrix = matrix
        self.depth = len(self.matrix)
        self.width = len(self.matrix[0])
        self.solution_ranks = [[0 for _ in range(self.width)] for _ in range(self.depth)]
        self.index_ranks = [0 for _ in range(self.depth+self.width)]
        self.values = self.create_values()
        self.edges = self.create_edges()

    def create_values(self):
        """Produce a sorted list of values that appear in the matrix."""
        values = set()
        for i in range(self.depth):
            for j in range(self.width):
                values.add(self.matrix[i][j])
        return sorted(list(values))

    def create_edges(self):
        eds = defaultdict(list)
        for i in range(self.depth):
            for j in range(self.width):
                val = self.matrix[i][j]
                eds[val].append((i, j))
        return eds

    def indexes(self, val):
        """Given a value, return the set of all indexes that have cells of that value"""
        ans = set()
        for i, j in self.edges[val]:
            ans.add(i)
            ans.add(j+self.depth)
        return ans

    def neighbours(self, val):
        """For a given value, construct the dictionary of index-neighbours"""
        ans = defaultdict(set)
        for i, j in self.edges[val]:
            ans[i].add(j+self.depth)
            ans[j+self.depth].add(i)
        return ans

    def generate_index_components(self, val):
        """Yield connected components of of indexes.

        Find groups of indexes that are connected i.e.
        whose cells with value val need to be assigned ranks simultaneously.
        This is a vanilla bfs component finder, using
        'indexes' for initializing the graph and
        'neighbours' for finding vertex neighbours.
        """
        # bfs
        inds = self.indexes(val)
        nbs = self.neighbours(val)
        while inds:
            start = inds.pop()
            q = deque()
            q.append(start)
            visited = {start}

            while q:
                v = q.popleft()
                visited.add(v)
                for w in nbs[v]:
                    if w not in visited:
                        q.append(w)
                        visited.add(w)
                        inds.remove(w)
            yield visited

    def process_component(self, component, val):
        # compute the rank
        r = max(self.index_ranks[index] for index in component)+1
        # assign the rank
        for i, j in self.edges[val]:
            if i in component or j+self.depth in component:
                self.solution_ranks[i][j] = r
                self.index_ranks[i] = r
                self.index_ranks[j+self.depth] = r

    def create_solution_ranks(self):
        for val in self.values:
            for component in self.generate_index_components(val):
                self.process_component(component, val)


class Solution:
    def matrixRankTransform(self, matrix: List[List[int]]) -> List[List[int]]:
        ranker = Ranker(matrix)
        ranker.create_solution_ranks()
        return ranker.solution_ranks
