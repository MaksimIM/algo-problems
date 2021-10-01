## Beautiful Arrangement

This is a solution for the Beautiful Arrangement problem, problem 526 on LeetCode:

https://leetcode.com/problems/beautiful-arrangement/

### The problem


Suppose you have `n` integers labeled `1` through `n`. A permutation of those `n` 
integers `perm`  is considered a **beautiful arrangement** if for every 
`i` `(1 <= i <= n)`, at least one of the following is true:

* `perm[i]` is divisible by `i`
* `i` is divisible by `perm[i]`.

The problem asks that for a give `n` we compute the number of possible beautiful arrangements.

### Some solutions

1) One way to view this problem is as a constraint satisfaction problem. Namely, 
we need to assign to each `(1 <= i <= n)` the value `perm[i]` subject to constraint
`(i % perm[i] == 0 OR perm[i] % i == 0)`. Thus, one can run a backtracking algorithm, 
assigning values to each of the `i`s and backtracking when no further assignment is 
possible. A concise algorithm implementing this approach was 
[posted](https://leetcode.com/problems/beautiful-arrangement/discuss/99738/Easy-Python-~230ms)
by Stefan Pochmann. He observes that the order of assignment is important: if one assigns 
`perm[i]` to `i=n` first, then to `i=n-1` etc., one gets faster algorithm than one would if one assigned in 
ascending order (first to `i=1`, then to `i=2` etc.). Of course, this is nothing 
but a version of 'most constrained first' heuristic - the high values tend to be more constrained since they 
don't have any multiples below `n`. Our first solution, **arrangement-backtrack.py**, 
implements as light modification of this, where we precompute all possible `perm[i]` for each `i` and also the 
degree to which each `i` is constrained, and then perform assignment in this order. 
Of course this is not 'real' implementation 'most constrained first' - we don't update
'the degree of constraintness' dynamically. Nonetheless, it gives some speed on the original implementation.


2) One can observe that in fact no backtracking is actually needed in this problem. 
If we construct the graph `G` in which each `i` is a vertex, and connect `i` to `j` 
precisely when  `(i % j == 0 OR j % i == 0)`, then a beautiful arrangement is
precisely a decomposition of this graph's vertices into disjoint cycles, known as a [vertex cycle cover](https://en.wikipedia.org/wiki/Vertex_cycle_cover).
General problem of counting vertex cycle covers in weighted directed graphs is [#P-Hard](http://people.csail.mit.edu/shaih/pubs/01perm.pdf). 
Of course this particular graph `G`  is very special; nonetheless, I do not know an efficient way to **count** vertex cycle covers in it either. 
We can, however, **generate** all of them without backtracking. Namely, we start from some vertex `v` and use a graph traversal
(DFS) to find all simple cycles in `G`  'from `v` to `v`'. For each such cycle, we remove all its vertices from `G` 
and recursively construct all vertex cycle covers of the result. This way we obtain all vertex cycle covers of `G`.
This algorithm is implemented in **arrangement-vertex-cover.py**. Unfortunately, the graph modifications needed 
(at least in naive implementations) slow down the algorithm and, despite not having to backtrack, it runs a bit slower than the first one.

3) The 'sum over permutations' nature of what we are counting is suggestive. Since 
the validity of permutation is determined only by condition relating `i` to `perm[i]`,
the answer is given by the [permanent](https://en.wikipedia.org/wiki/Permanent_(mathematics)) of the matrix  `M` whose entry `M_ij` is 1 if the condition holds and zero otherwise. 
[Computing the permanet](https://en.wikipedia.org/wiki/Computing_the_permanent) is, in general, difficult. However, there is a [formula](https://en.wikipedia.org/wiki/Computing_the_permanent#Balasubramanian%E2%80%93Bax%E2%80%93Franklin%E2%80%93Glynn_formula) 
for it which allows this to at least be done faster than by going over every permutation. An algorithm using this formula is in **arrangement-permanent.py**.

###Remarks

* Vertex cycle covers and permanents are, of course, very much [connected](https://en.wikipedia.org/wiki/Permanent_(mathematics)#Cycle_covers).
* By considering only permutations made up of transpositions, one can get a lower bound of about `2^(n^0.5)` on the answer. On the other hand, from [Bregman-Minc](https://en.wikipedia.org/wiki/Bregman%E2%80%93Minc_inequality)
one expects an upper bound of the type  `P(n) e^n`.
In reality, the answer seems to be growing slightly faster than `2^n` (first exceeding this when `n=16`). 

