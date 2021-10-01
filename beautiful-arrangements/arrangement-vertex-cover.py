import copy


class Solution(object):
    def countArrangement(self, n):
        # Build graph.
        graph = {i: set() for i in range(1, n+1)}
        for i in range(1, n+1):
            graph[i].add(i)
            for m in range(2*i, n+1, i):
                graph[m].add(i)
                graph[i].add(m)

        # Graph utilities.
        def remove_vertex(g, v):
            neighbors = copy.copy(g[v])
            for w in neighbors:
                g[w].remove(v)
            del g[v]

        def remove_vertices(g, vertices):
            for v in vertices:
                remove_vertex(g, v)

        def restore(g, diff):
            for v in diff:
                for w in diff[v]:
                    if w not in diff:
                        g[w].add(v)
                g[v] = diff[v]

        # Core computation.
        def find_cycles(g, i):
            cycles = []
            
            def dfs(u, v, visited):
                visited.add(u)
                for w in g[u]:
                    if w == v:
                        cycles.append(copy.copy(visited))
                    elif w not in visited:
                        dfs(w, v, visited)
                visited.remove(u)

            dfs(i, i, set())
            return cycles

        def count_vertex_cycle_covers(g):
            count = 0
            if not g:
                return 1
            else:
                v = next(iter(g))
                for cycle in find_cycles(g, v):
                    diff = {v: copy.copy(g[v]) for v in cycle}
                    remove_vertices(g, cycle)
                    count += count_vertex_cycle_covers(g)
                    restore(g, diff)
            return count

        return count_vertex_cycle_covers(graph)


if __name__ == '__main__':
    s = Solution()
    print(s.countArrangement(15))
