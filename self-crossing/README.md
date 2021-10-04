## Self Crossing

This is a solution for the Self Crossing, problem 335 on LeetCode:

https://leetcode.com/problems/self-crossing/

### The problem.

You are given an array of integers `distance`.

You start at point `(0,0)` on an `X-Y` plane and you move `distance[0]`
meters to the north, then `distance[1]` meters to the west, `distance[2]`
meters to the south, `distance[3]` meters to the east, and so on. 
In other words, after each move, your direction changes counter-clockwise.

Return `true` if your path crosses itself, and `false` if it does not.


### A solution.

Let curve C be formed as in the problem, by joining segments `s(i)` of length `d(i)`.

The intuition here is that a non-self-intersecting curve built this way is made of two spirals, first spiraling out with growing `d(i)`, and then spiraling in, with decreasing `d(i)` (of course one of those spirals may be empty).

**Theorem 1**:  Suppose C is not self-intersecting. Then either `d(i+2)>d(i)` for all `i`, or there exists I such that `d(i+2)>d(i)` for all `i<I, d(I+2)<=d(I)` and  `d(i+2)<d(i)` for all `i>I`. 
 
**Theorem 2**: If `d(i+2)>d(i)` for all `i` then `C` is not-self intersecting.
Suppose, on the other hand, there exists `I` such that `d(i+2)>d(i)`  for all `i<I`, `d(I+2)<=d(I)` and
  `d(i+2)<d(i)` for all `i>I`. Then, either (after possibly padding the path with 0-length segments so 
  that both `s(I-2)` and `s(I+3)` exist) segments `s(I-2)` and `s(I+3)` intersect, or `C` is not self-intersecting.
  
  **Corollary**: If `C` is self-intersecting, then either exists  `i` such that  `s(i)` intersects `s(i+3)` or exists  `i` such that `s(i)` intersects `s(i+5)`.
  

The theorems suggest a simple approach of going through the `distances` array looking for the step `I` when the switch from spiraling out to spiraling in happens, and then checking for intersection of `s(I-2)` and  `s(I+3)` (which can be done by considering the lengths of `s(I-2)`,`s(I-1)`,`s(I)`,`s(I+1)`,`s(I+2)`, and `s(I+3)` only). This is implemented in **self-crossing.py**.
  
Corollary also suggests an approach, in which one goes through the curve once checking for intersection of `s(i)` with `s(i+3)` and `s(i+5)` at ecery step. This is a popular approach on LeetCode.

### Proofs.


**Proof sketch of Theorem 1**: Suppose `C` is not self-intersecting.  Consider the smallest `I` such that `d(I+2)<=d(I)` (if there is no such then we are done). Then, possibly after rotation we have the picture like this:

>              |   
>          s(I)|        |
>              |_______ | s(I+2)
>                s(I+1)

 Thus, if `C` is not self intersecting,  `d(I+3)<d(I+1)`. By induction,  `d(i+2)<d(i)` for all `i>I`.
 
**Proof sketch of Theorem 2**:  Consider the initial part of `C`, consisting of the first `I+2`
 segments `s(0),..., s(I+1)`. This part "spirals out" and is not self-intersecting. More strongly,
 for any segment in this part, all previous segments lie to one side of that segment.
 (If the segment is running up, the previous ones are to the left, if its running left the previous ones are below etc. This can be proved by induction on the segment number, see Bonus Lemma 1 below.) Thus, the segment can never intersect any of the previous ones, and indeed that part of C is not self intersecting.
   
  If this is all of `C` (i.e. if `d(i+2)>d(i)` for all `i`), then the whole `C` is non-self intersecting.
   
If not, then consider the "end" part of `C` consisting of the segments `s(I+1),..., s(n)`, which "spiral in". By our assumption, it has `d(i+2)<d(i)`, but  if we retrace that part backwards, as `s(n), s(n-1), ... s(I+1)`,  will have `d(i+2)>d(i)` and will be like the initial part, except turning right instead of left. Thus, this part of `C` is also not self-intersecting and has the "segments after `s(j)` are to one side of `s(j)`" property as well.

Therefore, we have a picture like so:
  
>           s(I-1) 
>           _______              s(I+3)
>          |   ____|s(I-2)       _______
>      s(I)|   s(I-3)     s(I+4)|       |
>          |____________________________| s(I+2)
>                  s(I+1)
      
 with initial part of `C` inside the box made by part of `s(I)`, `s(I-1)`, `s(I-2)` and `s(I-3)` and the "end" part of `C` inside the box made by part of `s(I+1)`, `s(I-2)`, `s(I+3)` and `s(I+4)`. If these boxes don't intersect, then C is not self intersecting. But these boxes intersect precisely when  `s(I-2)` intersects `s(I+3)`.
    
**Proof of corollary**: We prove the contrapositive. Since `s(i+3)` intersects `s(i)` precisely when `d(i+2)<=d(i)` and `d(i+3)>=d(i)`,
    if this does not happen, then either `d(i+2)>d(i)` always, or as soon as `d(I+2)<=d(I)` for the first time we have `d(i+2)<d(i)` for all `i>I`. Thus, in either case, we are in the situation of Theorem 2.  But then by that Theorem, if `s(I-2)` does not intersect `s(I+3)` the curve is not self-intersecting. The corollary follows.
      
    
----

**Bonus**:

**Lemma 1**: Suppose  `d(i+2)>d(i)` for all `i<I`. Then for any segment `s(i)` with `i<I`:

0) if `s(i)` is going up (i.e. `i%4==0`), then the part of the curve up to `s(i)`
(i.e. `s(0)`,`s(1)`, ... , `s(i-2)`) lies strictly to the left of that segment 
(i.e. the x-coordinates of all points are less than those of the points of `s(i)`).

1) if s(i) is going left (i.e. `i%4==1`), then the part of the curve up to `s(i)`
(i.e. `s(0)`, `s(1)`, ... , `s(i-2)`) lies strictly below that segment 
(i.e. the y-coordinates of all points are less than those of the points of `s(i)`).

2) if s(i) is going down (i.e. `i%4==2`), then the part of the curve up to `s(i)`
(i.e. `s(0)`, `s(1)`, ... , `s(i-2)`) lies strictly to the left of that segment 
(i.e. the x-coordinates of all points are bigger than those of the points of `s(i)`).

3) if `s(i)` is going right (i.e. `i%4==3`), then the part of the curve up to `s(i)`
(i.e. `s(0)`, `s(1)`, ... , `s(i-2)`) lies strictly above that segment 
(i.e. the y-coordinates of all points are greater than those of the points of `s(i)`).




Proof:

0) Consider  `i=4k`. 
When `k=0` there is nothing to prove. We proceed by induction on `k`. 
Th segment `s(4k)` has x-coordinate `x(k)=-d(2)+d(4)-d(6)+...+d(4k)`, which is 
equal to `x(k-1)+(-d(4k-2)+d(4k))`. Since `d(4k)> d(4k-2)` by assumption, `x(k)>x(k-1)`.
Then by induction hypothesis, all the segments up to s(4k-5) have x-coordinates below 
`x(k-1)`, so below `x(k)` as well. Thus, we only need to worry about
 `s(4k-5)`, `s(4k-4)`, `s(4k-3)` and `s(4k-2)`. But all of these are (non-strictly) 
 to the left of `s(4k-4)`, and so all their points have x-coordinates `<=x(k-1) < x(k)`
 as well. This completes the proof.
 
 The proofs for all other cases are analogous (they are all "rotated versions" of each other.)



  
