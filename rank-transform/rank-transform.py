"""This is a solution for the Rank Transform of a Matrix problem.

This is problem 1632 on LeetCode
https://leetcode.com/problems/rank-transform-of-a-matrix/

The basic idea is simple:
going from lowest values to highest,
for a given value, find groups of cells with that value
that must have the same rank.
For a given group, that rank must be
one more than the maximal ranks already assigned
to cells in the rows and columns of the group.
Thus we assign this rank to all cells in the group,
do this for all groups and then move on to the next value.


A key optimization is to find the groups of cells of same rank
not by looking for connected components of the  graph whose vertices
are cells, but, rather, in a graph whose vertices are (row or column)
indexes. For a fixed value v, a vertex in this graph is any index such
that in the corresponding row or column there is a cell with value v.
This cell is then an edge between its row index and its column index.
All such cells that are edges in a connected component
of our graph need to be assigned their rank simultaneously.

Please see the README on this files github for further details.
"""
import copy
from abc import ABC
from abc import abstractmethod
from collections import defaultdict
from collections import deque
from typing import List, Iterable, DefaultDict, Hashable, Set

# Choose 'BFS', 'UF_SIZE', 'UF_RANK'
_VERSION = 'BFS'


class Solution:
    def matrixRankTransform(self, matrix: List[List[int]]) -> List[List[int]]:
        version_parameters = {
            'BFS': (EdgesToComponentsBFS,),
            'UF_SIZE': (EdgesToComponentsUF,
                        {'strategy_class': ComponentCollectionSizeBased}),
            'UF_RANK': (EdgesToComponentsUF,
                        {'strategy_class': ComponentCollectionRankBased}),
            }
        ranker = Ranker(matrix, *version_parameters[_VERSION])
        return ranker.solution


class Ranker:
    def __init__(self, matrix, component_maker_class,
                 component_maker_kwargs=None):
        self._matrix = matrix
        self._depth = len(self._matrix)
        self._width = len(self._matrix[0])
        self._index_ranks = [0 for _ in range(self._depth+self._width)]
        self._solution = None
        self._values = self._create_values()
        self._edges = self._create_edges()
        self._components_maker_class = component_maker_class
        if component_maker_kwargs is None:
            self._component_maker_kwargs = {}
        else:
            self._component_maker_kwargs = component_maker_kwargs

    def _create_values(self):
        """Produce a sorted list of values that appear in the matrix."""
        values = set()
        for i in range(self._depth):
            for j in range(self._width):
                values.add(self._matrix[i][j])
        return sorted(list(values))

    def _create_edges(self):
        eds = defaultdict(list)
        for i in range(self._depth):
            for j in range(self._width):
                val = self._matrix[i][j]
                eds[val].append((i, j+self._depth))
        return eds

    @property
    def solution(self):
        if not self._solution:
            self._solution = [[0 for _ in range(self._width)]
                              for _ in range(self._depth)]
            for val in self._values:
                for component in self._components(val):
                    self._update_ranks(component)
                self._assign_ranks(val)
        return self._solution

    def _components(self, val):
        return self._components_maker_class(
            self._edges[val], **self._component_maker_kwargs).components()

    def _update_ranks(self, component):
        # compute the rank
        r = max(self._index_ranks[index] for index in component)+1
        # update the rank
        for index in component:
            self._index_ranks[index] = r

    def _assign_ranks(self, val):
        for i, j_shifted in self._edges[val]:
            j = j_shifted-self._depth
            self._solution[i][j] = self._index_ranks[i]


class EdgesToComponentsBase(ABC):
    def __init__(self, edges):
        self._edges = edges
        self._vertices = self._get_vertices()

    @abstractmethod
    def components(self) -> Iterable:
        pass

    def _get_vertices(self):
        vertices = set()
        for i, j in self._edges:
            vertices.add(i)
            vertices.add(j)
        return vertices


class EdgesToComponentsBFS(EdgesToComponentsBase):

    def components(self) -> Iterable:
        """A vanilla bfs component finder method."""

        # Construct the dictionary of neighbours.
        v_to_nbrs = self._vertex_to_neighbours()
        # BFS
        # Copy the vertices or use them up?
        # We copy, even if using up is a bit faster.
        remaining_vertices = copy.copy(self._vertices)
        while remaining_vertices:
            start = remaining_vertices.pop()
            q = deque([start])
            visited = {start}

            while q:
                v = q.popleft()
                visited.add(v)
                for w in v_to_nbrs[v]:
                    if w not in visited:
                        q.append(w)
                        visited.add(w)
                        remaining_vertices.remove(w)
            yield visited

    def _vertex_to_neighbours(self) -> DefaultDict[Hashable, Set]:
        v_to_nbrs = defaultdict(set)
        for i, j in self._edges:
            v_to_nbrs[i].add(j)
            v_to_nbrs[j].add(i)
        return v_to_nbrs


class EdgesToComponentsUF(EdgesToComponentsBase):
    def __init__(self, edges, strategy_class):
        super().__init__(edges)
        self._strategy_class = strategy_class

    def components(self) -> Iterable:
        """A union-find-based component finder method."""

        # create graph
        graph = self._strategy_class(self._get_vertices())
        # add edges
        for i, j in self._edges:
            graph.union(i, j)
        return graph.component_list()


class ComponentCollection(ABC):
    """The union-find data structure.

    Maintains a collection of connected components as an implicit set of trees.
    Allows finding a representative (root) of a component
    and merging two components.
    """
    def __init__(self, components):
        self._node_to_parent = {c: c for c in components}

    @abstractmethod
    def find_root(self, c):
        pass

    @abstractmethod
    def union(self, c1, c2):
        pass

    def component_list(self):
        components = defaultdict(list)
        for node in self._node_to_parent:
            components[self.find_root(node)].append(node)
        return components.values()


class ComponentCollectionRankBased(ComponentCollection):
    def __init__(self, components):
        super().__init__(components)
        self._node_to_rank = {c: 0 for c in components}  # max depth to a leaf

    def find_root(self, c):
        # with path compression, that is
        # every root-finding call changes all parents in the path to be the root
        if self._node_to_parent[c] == c:
            return c
        else:  # make parent be the (recursively found) root and return it
            self._node_to_parent[c] = self.find_root(self._node_to_parent[c])
        return self._node_to_parent[c]

    def union(self, c1, c2):
        root1, root2 = self.find_root(c1), self.find_root(c2)
        if root1 != root2:
            # make shallower tree a subtree of a deeper one
            rank1, rank2 = self._node_to_rank[root1], self._node_to_rank[root2]
            if rank1 > rank2:
                root1, root2 = root2, root1
                rank1, rank2 = rank2, rank1
            self._node_to_parent[root1] = root2
            # if equally deep, the depth of the union is higher by 1
            if rank1 == rank2:
                self._node_to_rank[root2] = rank2+1


class ComponentCollectionSizeBased(ComponentCollection):
    def __init__(self, components):
        super(ComponentCollectionSizeBased, self).__init__(components)
        self._parent_to_nodes = {c: {c} for c in components}

    def find_root(self, c):
        return self._node_to_parent[c]

    def union(self, c1, c2):
        root1, root2 = self.find_root(c1), self.find_root(c2)
        if root1 != root2:
            size1, size2 = len(self._parent_to_nodes[root1]), \
                           len(self._parent_to_nodes[root2])
            # make root1 smaller
            if size1 > size2:
                root1, root2 = root2, root1
            # merge trees
            self._node_to_parent[root1] = root2
            # repoint all children of root1
            for child in self._parent_to_nodes[root1]:
                self._node_to_parent[child] = root2
            # update children dict
            self._parent_to_nodes[root2].update(self._parent_to_nodes[root1])
            del self._parent_to_nodes[root1]


def main():
    matrix = [
            [20,-21,14],
            [-19,4,19],
            [22,-47,24],
            [-19,4,19]
            ]

    sol = Solution()
    ranks=sol.matrixRankTransform(matrix)
    for row in ranks:
        print(row)


if __name__ == '__main__':
    main()
