class Solution(object):

    def countArrangement(self, N):
        if N < 4:
            return N
        graph = {i: [] for i in range(1, N+1)}
        for i in range(1, N+1):
            graph[i].append(i)
            for m in range(2*i, N+1, i):
                graph[m].append(i)
                graph[i].append(m)

        order=sorted(range(1, N+1), key=lambda x: len(graph[x]))

        def count(i, X):
            j = order[i]
            if j == 1:
                return 1
            return sum(count(i+1, X - {x})
                    for x in graph[j]
                    if x in X)

        return count(0, set(range(1, N + 1)))


if __name__ == '__main__':
    from math import log2
    s = Solution()
    for i in range(1,23):
        a=s.countArrangement(i)
        print( a, i, log2(a))

