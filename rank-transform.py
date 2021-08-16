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

It is important that for each v we initialize the graph
to have only the vertices (indexes) that actually contain cells
with value v. Then the number of vertices will be at most twice the number of edges,
and the component search will take O(V+E)=O(E) for each value, if done via
a BFS or a DFS graph exploration algorithm.
Summing over all values, we see that finding components
is will take time linear in the number of cells involved, C.

An alternative implementation that uses a union-find sata structure instead.
When fully optimized, it performs component-finding in O(C alpha(C)) time.
Here alpha is the inverse Ackermann function,
which is at most 4 for all practical input sizes
(an n for which alpha(n)>4 would require more bits to write down
than there are atoms in the universe).

We provide both implementations, via EdgesToComponentsBFS and EdgesToComponentsUF classes,
which both inherit from abstract EdgesToComponentsBase and provide their own implementations
of the generate_components method. Furthermore, we implement both size-based and rank-based
union strategies for the union-find version.

Their time performance of all three versions are not too different,
(the BFS version is a bit faster, landing consistently in 99th percentile on LeetCode),
though the union-find version uses less memory
(because it does not need to maintain neighbor-dictionary versions of the graphs),
For the size-based union strategy the time is quite close to that of the BFS version.

Overall, the worst-case complexity of each implementation is O(C ln C),
due to the sorting of the matrix values.
After that step the rest runs in
O(C) (BFS)/O(C alpha(C)) (rank-based UF)/O(C ln(C)) (size-based UF)
time.

Some final notes:

0) To have a fast rank-assignment method, we maintain a lookup table of
currently maximal ranks in each row/column. The rank of a component is then
one more than the maximal rank already present.
1) In the union-find version, to maintain sub-cubic (in N) complexity
one needs at least one optimization in component finding,
either merge-by-size or merge by rank, to ensure logarithmic time
for find and union operations. To obtain the O(C alpha(C)) complexity,
union by rank with path compression is needed. In practice,
path compression makes little difference on the LeetCode examples.
2) There are some alternative approaches to implementing the BFS version.
For example, instead of the sets of edges, one could directly build two dictionaries,
one mapping a value to all the indexes relevant to that value (aka the vertices
of the corresponding graph) and one mapping and index-vertex (and a value)
to all its neighbors. This has similar performance but would make the BFS/DFS
implementation diverge more from the union-find one. So we stick to the
"dictionary of edges" version (and generate neighbours when needed).
"""
import copy
from collections import deque
from collections import defaultdict
from abc import ABC, abstractmethod
from typing import List, Iterable, DefaultDict, Hashable, Set

# Choose 'BFS', 'UF_SIZE', 'UF_RANK'
version = 'BFS'


class Solution:
    def matrixRankTransform(self, matrix: List[List[int]]) -> List[List[int]]:
        version_parameters = {
            'BFS': [EdgesToComponentsBFS],
            'UF_SIZE': [EdgesToComponentsUF,
                        {'strategy_class': ComponentCollectionSizeBased}],
            'UF_RANK': [EdgesToComponentsUF,
                        {'strategy_class': ComponentCollectionRankBased}],
            }

        ranker = Ranker(matrix, *version_parameters[version])
        ranker.create_solution_ranks()
        return ranker.solution_ranks


class Ranker:
    def __init__(self, matrix, component_maker_class, component_maker_kwargs=None):
        self.matrix = matrix
        self.depth = len(self.matrix)
        self.width = len(self.matrix[0])
        self.solution_ranks = [[0 for _ in range(self.width)] for _ in range(self.depth)]
        self.index_ranks = [0 for _ in range(self.depth+self.width)]
        self.values = self.create_values()
        self.edges = self.create_edges()
        self.components_maker_class = component_maker_class
        if component_maker_kwargs is None:
            self.component_maker_kwargs = {}
        else:
            self.component_maker_kwargs = component_maker_kwargs

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
                eds[val].append((i, j+self.depth))
        return eds

    def create_solution_ranks(self):
        for val in self.values:
            for component in self.components(val):
                self.update_ranks(component)
            self.assign_ranks(val)

    def components(self, val):
        return self.components_maker_class(self.edges[val],
                                           **self.component_maker_kwargs).components()

    def update_ranks(self, component):
        # compute the rank
        r = max(self.index_ranks[index] for index in component)+1
        # update the rank
        for index in component:
            self.index_ranks[index] = r

    def assign_ranks(self, val):
        for i, j_shifted in self.edges[val]:
            j = j_shifted-self.depth
            self.solution_ranks[i][j] = self.index_ranks[i]


class EdgesToComponentsBase(ABC):
    def __init__(self, edges):
        self.edges = edges
        self.vertices = self.get_vertices()

    @abstractmethod
    def components(self) -> Iterable:
        pass

    def get_vertices(self):
        vertices = set()
        for i, j in self.edges:
            vertices.add(i)
            vertices.add(j)
        return vertices


class EdgesToComponentsBFS(EdgesToComponentsBase):

    def components(self) -> Iterable:
        """A vanilla bfs component finder method."""

        # Construct the dictionary of neighbours.
        v_to_nbrs = self.vertex_to_neighbours()
        # BFS
        # Copy the vertices or use them up? We copy, even if using up is a bit faster.
        remaining_vertices = copy.copy(self.vertices)

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

    def vertex_to_neighbours(self) -> DefaultDict[Hashable, Set]:
        v_to_nbrs = defaultdict(set)
        for i, j in self.edges:
            v_to_nbrs[i].add(j)
            v_to_nbrs[j].add(i)
        return v_to_nbrs


class EdgesToComponentsUF(EdgesToComponentsBase):
    def __init__(self, edges, strategy_class):
        super(EdgesToComponentsUF, self).__init__(edges)
        self.strategy_class = strategy_class

    def components(self) -> Iterable:
        """A union-find-based component finder method."""

        # create graph
        graph = self.strategy_class(self.get_vertices())
        # add edges
        for i, j in self.edges:
            graph.union(i, j)
        return graph.component_list()


class ComponentCollection(ABC):
    def __init__(self, components):
        self.node_to_parent = {c: c for c in components}

    @abstractmethod
    def find_root(self, c):
        pass

    @abstractmethod
    def union(self, c1, c2):
        pass

    def component_list(self):
        components = defaultdict(list)
        for node in self.node_to_parent:
            components[self.find_root(node)].append(node)
        return components.values()


class ComponentCollectionRankBased(ComponentCollection):
    """The union-find data structure.

    Maintains a collection of connected components as an implicit set of trees.
    Allows finding a representative (root) of a component and merging two components.
    """
    def __init__(self, components):
        super(ComponentCollectionRankBased, self).__init__(components)
        self.node_to_rank = {c: 0 for c in components}  # max depth to a leaf from c

    def find_root(self, c):
        # with path compression, that is
        # every root-finding call changes all parents in the path to be the root
        if self.node_to_parent[c] == c:
            return c
        else:  # make parent be the (recursively found) root and return it
            self.node_to_parent[c] = self.find_root(self.node_to_parent[c])
        return self.node_to_parent[c]

    def union(self, c1, c2):
        root1, root2 = self.find_root(c1), self.find_root(c2)
        if root1 != root2:
            # make shallower tree a subtree of a deeper one
            rank1, rank2 = self.node_to_rank[root1], self.node_to_rank[root2]
            if rank1 > rank2:
                root1, root2 = root2, root1
                rank1, rank2 = rank2, rank1
            self.node_to_parent[root1] = root2
            # if equally deep, the depth of the union is higher by 1
            if rank1 == rank2:
                self.node_to_rank[root2] = rank2+1


class ComponentCollectionSizeBased(ComponentCollection):
    """The union-find data structure.

    Maintains a collection of connected components as an implicit set of trees.
    Allows finding a representative (root) of a component and merging two components.
    """
    def __init__(self, components):
        super(ComponentCollectionSizeBased, self).__init__(components)
        self.parent_to_nodes = {c: {c} for c in components}

    def find_root(self, c):
        return self.node_to_parent[c]

    def union(self, c1, c2):
        root1, root2 = self.find_root(c1), self.find_root(c2)
        if root1 != root2:
            size1, size2 = len(self.parent_to_nodes[root1]), len(self.parent_to_nodes[root2])
            # make root1 smaller
            if size1 > size2:
                root1, root2 = root2, root1
            # merge trees
            self.node_to_parent[root1] = root2
            # repoint all children of root1
            for child in self.parent_to_nodes[root1]:
                self.node_to_parent[child] = root2
            # update children dict
            self.parent_to_nodes[root2].update(self.parent_to_nodes[root1])
            del self.parent_to_nodes[root1]
