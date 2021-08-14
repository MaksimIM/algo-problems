"""This is an implementation of matrix rank transform using
a union-find data structure.

It iterates over values in the matrix from lowest to highest.
For each value, it uses union-find to generate components
of the set of indexes (sic!). In this graph the edges are
matrix entries having the  current value.
The entry (i,j) connects the indexes i and j.
All the entries corresponding to each index-connected-component
are assigned the same rank, which is one more than
the maximal rank of all their row and column indexes.

The time complexity is dominated by sorting the values,
which, at worst, is an O(C log C) operation (here C is the number of entries
in the matrix).
After that the algorithms complexity is dominated by the generation
of connected components, which runs in O(C alpha(C)) time. Here alpha is
the inverse Ackermann function, which is at most 4 for all input sizes
(an n for which alpha(n)>4 would require more bits to write down
than there are atoms in the universe).
"""
from collections import defaultdict
from typing import List


class ComponentCollection:
    """The union-find data structure.
    Maintains a collection of connected components as an implicit set of trees.
    Allows finding a representative (root) of a component and merging two components."""
    def __init__(self, components):
        self.parent = {c: c for c in components}
        self.rank = {c: 0 for c in components}  # max depth to a leaf from c

    def find_root(self, c):
        # with path compression, that is
        # every root-finding call changes all parents in the path to be the root
        if self.parent[c] == c:
            return c
        else:  # make parent be the (recursively found) root and return it
            self.parent[c] = self.find_root(self.parent[c])
        return self.parent[c]

    def union(self, c1, c2):
        root1, root2 = self.find_root(c1), self.find_root(c2)
        if root1 != root2:
            # make shallower tree a subtree of a deeper one
            rank1, rank2 = self.rank[root1], self.rank[root2]
            if rank1 > rank2:
                root1, root2 = root2, root1
                rank1, rank2 = rank2, rank1
            self.parent[root1] = root2
            # if equally deep, the depth of the union is higher by 1
            if rank1 == rank2:
                self.rank[root2] = rank2+1

    def dict_of_components(self):
        component = defaultdict(list)
        for node in self.parent:
            component[self.find_root(node)].append(node)
        return component


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

    def generate_index_components(self, val):
        """Yield connected components of indexes.

        Find groups of indexes that are connected i.e.
        whose cells with value val need to be assigned ranks simultaneously.
        This is a vanilla bfs component finder, using
        'indexes' for initializing the graph and
        'neighbours' for finding vertex neighbours.
        """
        # create graph
        graph = ComponentCollection(self.indexes(val))
        # add edges
        for i, j in self.edges[val]:
            graph.union(i, j+self.depth)
        return graph.dict_of_components()

    def update_ranks(self, component):
        # compute the rank
        r = max(self.index_ranks[index] for index in component)+1
        # update the rank
        for index in component:
            self.index_ranks[index] = r

    def assign_ranks(self, val):
        for i, j in self.edges[val]:
            self.solution_ranks[i][j] = self.index_ranks[i]

    def create_solution_ranks(self):
        for val in self.values:
            for component in self.generate_index_components(val).values():
                self.update_ranks(component)
            self.assign_ranks(val)


class Solution:
    def matrixRankTransform(self, matrix: List[List[int]]) -> List[List[int]]:
        ranker = Ranker(matrix)
        ranker.create_solution_ranks()
        return ranker.solution_ranks
