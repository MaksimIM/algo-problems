## The Number of Good Subsets

This is a solution for the Number of Good Subsets, problem 1994 on LeetCode:

https://leetcode.com/problems/the-number-of-good-subsets/

### The problem


You are given an integer array `nums`. We call a subset of `nums` **good** if
its product can be represented as a product of one or more distinct prime numbers
(that is, this product is 
[square-free](https://en.wikipedia.org/wiki/Square-free_integer) 
and is not equal to `1`). 

Return the **number of different good subsets** in `nums` modulo `10^9 + 7`.


Constraints:
* `1 <= nums.length <= 10^5` 
* `1 <= nums[i] <= 30`

### Some solutions

##### Dynamic programming

Observe that we can pick any number of ones to be or not be in out good subset.
This means that if we count the number of good subsets without any 1s, 
the final answer will be just that count multiplied by `2^(count(1))`.  
With this proviso, we ignore any `1`s in `nums` from now on.

Now, to select a good subset, each number we pick must be square-free, and we can 
only pick one copy of each number.  Moreover, some numbers are incompatible with others.
To keep track, instead of just counting the ways to make a square-free product, we 
count the number of ways to make products **equal to each specific product of 
primes we can conceivably get**.
That is, for every subset `S` of primes below 30, we see how many ways we can
pick a subset of `nums` that multiplies to `S`. We can think of the subset 
of primes that appear in the product as a state, and when we decide to use a new 
number in the product we transition to a new state. We can compute the number 
of ways to reach every final state by sequentially deciding  to use or not use each  
square-free number n. In other words, if the set of primes into which n decomposes is S_n then
for each subset of primes S containing S_n we have:

 the number of ways to get subset S of primes using numbers up to and **in**cluding n =
 the number of ways to get  S using numbers up to and **ex**cluding n +
 the number of ways to get subset S-S_n using numbers up to and **ex**cluding n * the number of ways to pick n from `nums`

Of course, for all other subsets (those not containing S_n) we can not use n.

Using bitmasks to index subsets of primes, one gets from this a dynamic programming solution,
implemented in **good-subsets-dp.py**. One has to not forget to subtract 1 for 
the empty set (which leads to the product of 1, which the problem excludes), and to multiply by `2^#1s`
to account for all the `1`s that can be used as well.

##### A formula

Alternatively, we observe the following. 
If one only used prime numbers in the good subset, then the number of ways to do so would be 
the product of  `1+count(p)` over all primes p. However, we are allowed to use numbers that are products of primes.
If we use only one such number, say `p_1p_2`, then we can not use any of the `p`s or `q`s.
The count of such subsets is `count(p_1p_2)` times product of  `1+count(p)` over all primes `p` not equal to `p_1` or `p_2`.
We can rewrite this as `count(p_1p_2)/(1+count(p_1))(1+count(p_2))` times product of  `1+count(p)` over all primes `p`.
Combining this with the previous count we get

`(1+ sum [count(p_1p_2)/(1+count(p_1))(1+count(p_2))]) * (product (1+count(p)))`

Moreover, we can use more than one of the numbers `p_1p_2`, say `p_1p_2` and `q_1q_2`, as long as all of the 
`p_1`, `p_2`, `q_1`, `q_2` are all different. This adds another collection of terms. One more term comes from the possibility of 
using a product of 3 distinct primes, but, luckily, there is only one such not exceeding `30`, namely `30` itself.
Similarly, there is no way to use product of 3 numbers of the form `p_1p_2`. This means that no "higher" terms are needed.

Overall, we define

<img src="https://latex.codecogs.com/gif.latex?r_{p_i&space;p_j}&space;:=\frac{&space;n(p_i&space;p_j)}{(1&plus;n(p_i))(1&plus;n(p_j))}" title="r_{p_i p_j} :=\frac{ n(p_i p_j)}{(1+n(p_i))(1+n(p_j))}" />

```math
r_{p_i p_j} :=\frac{ n(p_i p_j)}{(1+n(p_i))(1+n(p_j))} 
```

<img src="https://latex.codecogs.com/gif.latex?r_{30}&space;:=&space;\frac{n(30)}{(1&plus;n(2))(1&plus;n(3))(1&plus;n(5))}" title="r_{30} := \frac{n(30)}{(1+n(2))(1+n(3))(1+n(5))}" />

```math
r_{30} := \frac{n(30)}{(1+n(2))(1+n(3))(1+n(5))}
```

and get the answer

<img src="https://latex.codecogs.com/gif.latex?2^{n(1)}\left[\prod_i&space;(1&plus;n(p_i))&space;\left(1&plus;\sum_{i>j}&space;r_{p_i&space;p_j}&space;&plus;&space;(r_{22}&plus;r_{26})(r_{15}&plus;r_{21})&plus;r_{15}r_{14}&plus;r_{21}r_{10}&space;&plus;r_{30}\right)&space;-1\right]" title="2^{n(1)}\left[\prod_i (1+n(p_i)) \left(1+\sum_{i>j} r_{p_i p_j} + (r_{22}+r_{26})(r_{15}+r_{21})+r_{15}r_{14}+r_{21}r_{10} +r_{30}\right) -1\right]" />

```math
2^{n(1)}\left[\prod_i (1+n(p_i)) \left(1+\sum_{i>j} r_{p_i  p_j} + (r_{22}+r_{26})(r_{15}+r_{21})+r_{15}r_{14}+r_{21}r_{10} +r_{30}\right)   -1\right].
```
The result can be computed using exact arithmetic of rational fractions. This is implemented in **good-subsets-math.py**.

#### Remarks

* In terms of speed, counting the occurrences of square-free 
numbers in `nums` is the slowest part in either method. 
After that, the two methods are compatible on speed. 
The dynamic programming method is straightforwardly extended 
to larger maximal numbers, but both time and space complexity 
is exponential in the number of relevant primes. 
The formula can also be extended, 
but doing it by hand does not scale, and doing it algorithmically
without exponential cost of going through every possible 
way of getting every possible subset of the primes would require 
some new ideas.

