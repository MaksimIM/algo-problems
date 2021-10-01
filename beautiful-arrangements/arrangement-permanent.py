import numpy as np


# https://github.com/scipy/scipy/issues/7151

def npperm(M):
    n = M.shape[0]
    d = np.ones(n)
    j = 0
    s = 1
    f = np.arange(n)
    v = M.sum(axis=0)
    p = np.prod(v)
    while j < n-1:
        v -= 2*d[j]*M[j]
        d[j] = -d[j]
        s = -s
        prod = np.prod(v)
        p += s*prod
        f[0] = 0
        f[j] = f[j+1]
        f[j+1] = j+1
        j = f[0]
    return p/2**(n-1)


class Solution(object):
    def countArrangement(self, n):
        M = np.zeros([n, n])
        for i in range(0, n):
            M[i, i] = 1
            for m in range(2*(i+1)-1, n, i+1):
                M[i, m] = 1
                M[m, i] = 1
        return int(npperm(M))


if __name__ == '__main__':
    sol = Solution()
    print(sol.countArrangement(15))
