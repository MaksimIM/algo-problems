## Largest Rectangle in Histogram

This is a solution for the Largest Rectangle in Histogram, problem 84 on LeetCode:

https://leetcode.com/problems/largest-rectangle-in-histogram/

### The problem.

Given an array of integers `heights` representing the histogram's bar height 
where the width of each bar is 1, 
return the area of the largest rectangle in the histogram.


### Some solutions.

We assume that we need to look at every "maximal" rectangle. 
Here "maximal" means not extendable right or left.
(I say "assume", since it's possible that we don't, 
but then we would need to exclude some maximal rectangles
a priori, which seems challenging.) The question, then,
is how to arrange for such an examination. One of our approaches (dp/bottlenecks)
produces and algorithm whose **time complexity is non-trivial to analyze**, 
which we do towards the end. 


#### Option 1: a sweep.
One idea is to do a sweep: moving left to right, activate a rectangle 
when it starts, and deactivate it when it ends. This suggests maintaining 
a stack of active rectangles, naturally arranged in increasing order of height.
When we encounter a new height, all rectangles that are taller than this height
need to be deactivated 
(which means that we compute their area and update maximal are if needed).
All other rectangles (shorter or equal than the new height)
are extended. If needed, a new rectangle starting from this location
is added to the stack. 

One option is to record the active rectangle as a pair (starting location, height).
But it is possible to make do with only one number - the location of the rightmost
bar with height equal to the height of the rectangle. For a given rectangle,
I will call bars in it which have height equal to the rectangle height **bottlenecks**.
So we store the rightmost bottleneck locations.
Then the height itself is
reconstructed by accessing `heights` at this location, and the start of the
rectangle is one to the right of the rightmost bottleneck 
for the previous rectangle(!). Finally, to avoid special "endpoint"
cases we append to `heights` an extra bar of zero (or any negative) height,
and we initiate the "active rectangle" stack with a "fake" 
rectangle starting at location `-1`
It automatically gets height `heights[-1] = 0`. 
This is what is done in the code of `rectangle-histogram-stack.py`.



Suppose the length of `heights` is `N`.
Since any location can be a start of at most one rectangle 
and an end to at most one rectangle, the total number or activating 
and deactivating operations is at most `N`, and hence the whole 
algorithm runs in `O(N)` time. It is also `O(N)` in space.

#### Option 2: Bottlenecks.

Another approach is based on the fact that every maximal rectangle has some 
bottleneck bar, and conversely, for each bar we can find a maximal rectangle
for which it is a bottleneck. If we can do this efficiently, this will
give us a way to look through all maximal rectangles.

To find a maximal rectangle for which given bar is a bottleneck, 
we should extend the rectangle from the bar's location as much as possible 
to the right and to the left. 

To extend to the left, we proceed in a recursive way 
(i.e. use dynamic programming). We look one step left. If the resulting bar
is shorter than the current one, the rectangle is not extendable. However,
if it is as tall or taller, then we can immediately jump to 
its maximal left extension, and proceed from there (look one to the left, 
see is the bar there is shorter or taller etc.), 
repeating until we encounter a shorter bar or reach the start of the array.

Extending to the right is similar, and one extra pass computes the areas 
and picks the largest one. This is implemented in `rectangle-histogram-dp.py`.

#### Complexity.

We now analyze the time complexity of this algorithm, and more specifically 
its part which computes  the maximal left extension. 
We will show that it runs in `O(N)` time, 
and hence the whole algorithm does as well.

Assume that all bar heights are distinct. This entails no loss of generality:
if there are bars of equal height, we can always add small (rational) 
amounts to their heights, in decreasing quantity going left to right, 
which would result in the same running of the algorithm (and we can rescale
resulting heights to be integer if desired). 
Thus the general case reduces to that where all heights are distinct. 
Moreover, since the running of the algorithm is affected only by which
bars are higher or lower than others and not by the actual heights, 
we can assume that the heights are a permutation of `0, ..., N-1`.

Then we have the following formula for the number of times 
the computation of maximal left extensions will extend the rectangles leftward.
Starting from the location of `0`, find the smallest height to the right of it,
and then recurse (find the smallest height higher than the current
height to the right of the current location, etc.) until you reach the end of 
the permutation. Call each iteration of this process a "rightward move".




**Theorem**: Given a permutation `p`
 the number of times the computation of maximal left extensions
will extend the rectangles leftward is `N-1` minus the number of rightward moves
(starting from the location of `0`).

This can be experimentally checked by running `complexity-analysis-dp.py`

**Proof**: By induction. This is true when `N=1` (and the answer is 0). 
Suppose now that in `p` the `0` in position `i` (0-based). Then there are two cases:
1) `i<N-1`. Then, by induction hypothesis, computing maximal left 
extensions in the first `i+1` rectangles
takes exactly `i` extensions. Also by induction hypothesis computing 
 maximal left 
extensions in the last `N-i-1` rectangles takes (`N-i-2` - number of right moves
after the first right move from `0`)=(`N-i-1` - number of right moves
from `0`) left extensions. In total, we need `i+N-i-1`-number of right moves
from `0` = N -1 - number of right moves
from `0` left extensions, аs claimed.
2) `i=N-1`. Then, by induction hypothesis,
to compute the maximal left extensions of the first `N-1` rectangles we need
(`N-2`- number of right moves from 1) left extensions. To extend the last
(0-height) rectangle, we precisely have to retrace the right moves from `1` in 
reverse order, plus make one last extension to the start of the permutation:
we start with height at location `N-2` which is the result of the
last right move, then all the heights 
between it and the start of the last right move are taller, so we 
extend the rectangle of height 0  exactly to the start of the last right move, 
and keep going until we reach 1 - and extend our rectangle of height 0 all the way
to teh start of the permutation.

Thus the total number of left extensions is
(`N-2`- number of right moves from 1)+(number of right moves from 1+1)=N-1.
Since in this case the number of right moves from 0 is 0, we get what we want.


This completes the proof, and we get that the running time of computing left
extensions - and hence of the whole second approach - is `O(N)`.





