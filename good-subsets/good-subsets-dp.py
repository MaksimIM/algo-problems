from collections import Counter

class Solution:
    def numberOfGoodSubsets(self, nums):
        mod = (10**9+7)
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        masks = {p: pow(2,i) for i, p in enumerate(primes)}

        for p in primes:
            for q in primes:
                if p > q and p*q < 30:
                    masks[p*q] = masks[p]+masks[q]
        masks[30] = 7

        counts = Counter(nums)
        dp = [1] + [0] * (pow(2, len(primes))-1)

        for n in masks:
            mask_n = masks[n]
            for mask in range(pow(2, len(primes))):
                if not (mask & mask_n):
                    dp[mask | mask_n] = (dp[mask | mask_n] + counts[n] * dp[mask]) % mod

        return ((sum(dp)-1) * pow(2, counts[1])) % mod


if __name__ == "__main__":
    s=Solution()
    ns = [1,26,1,1,21,1,3,13,1,1,1,26,29,29,6,10,29,1,1,11,15,6,14,1,17,1,1,30,
         1,17,1,1,1,23,1,7,17,15,1,1,1,14,22,11,22,17,1,19,1,2,21,29,1,22,1,1,14,
         22,1,14,1,1,1,1,17,1,1,1,3,1,14,19,1,1,1,1,21,26,1,1,1,13,1,1,30,21,1,1,
         1,1,7,1,1,7,13,6,1,29,29,1,1,23,1,19,10,10,1,1,2,1,1,23,15,5,15,1,1,19,
         15,1,1,14,1,7,26,1,1,2,13,19,1,3,22,1,1,29,1,7,1,1,1,1,3,1,1,1,3,1,1,1,
         2,17,1,1,1,1,1,19,5,1,1,1,19,30,23,1,1,2,1,1,7,17,1,1,1,30,21,1,3,1,5,
         15,1,26,1,1,21,22,19,1,13,6,15,19,2,1,1,1,1,11,17,21,29,23,26,10,1,30,1,
         14,1,1,21,1,30,1,1,1,11,22,19,21,30,11,14,1,1,3,7,17,10,10,3,1,1,1,10,1,
         15,1,15,15,1,1,1,1,1,21,14,6,1,17,1,1,1,17,10,3,1,22,21,1,1,23,19,1,5,5,
         5,10,1,29,1,1,1,1,7,1,15,1,6,6,1,1,1,13,1,1,29,17,1,1,1,6,1,1,2,13,10,
         29,1,13,21,7,10,1,1,1,7,29,15,29,17,5,30,1,11,1,23,1,1,1,5,1,30,6,1,5,6,
         1,11,17,26,1,1,13,1,26,1,11,13,1,11,1,1,1,30,1,1,1,14,19,1,1,15,21,1,1,
         2,1,1,19,1,26,1,5,22,13,1,1,11,7,29,3,26,30,19,10,1,7,1,22,1,6,2,1,23,
         26,1,11,11,5,1,1,1,5,6,7,21,1,1,10,1,1,29,1,1,6,19,1,1,5,1,30,1,15,1,3,
         15,15,23,6,1,5,1,1,1,1,3,1,1,17,7,1,11,6,13,2,17,1,3,1,22,1,1,23,13,1,3,
         1,1,1,1,13,22,1,22,1,10,1,23,15,14,1,30,1,1,29,17,3,1,19,1,7,14,2,1,14,
         23,2,30,1,19,1,1,10,19,23,1,1,1,1,1,1,1,1,1,1,1,26,30,26,1,2,2,21,1,1,1,
         1,1,1,1,1,1,22,15,21,15,13,26,1,1,1,1,21,1,13,30,1,22,1,14,1,21,15,14,
         21,1,22,1,1,1,11,1,6,6,1,1,1,13,3,10,23,15,30,1,1,7,19,7,1,30,15,1,7,1,
         11,2,17,14,17,21,1,1,17,1,3,23,1,1,11,21,1,1,1,1,10,1,11,1,1,1,1,6,22,1,
         1,6,26,23,1,1,11,10,1,6,6,1,26,1,1,1,1,1,1,1,1,1,22,1,19,13,1,1,2,10,1,
         26,1,1,5,3,10,13,11,17,1,1,23,1,7,5,1,1,11,22,1,23,1,1,1,29,26,2,1,19,
         15,13,29,1,1,19,26,1,11,26,11,1,6,1,1,26,21,3,2,1,1,10,1,1,21,15,1,1,23,
         1,2,5,1,3,1,1,1,14,5,1,21,1,30,11,5,21,14,14,1,1,19,10,1,1,1,1,22,14,1,
         7,23,1,29,23,1,1,1,17,1,1,1,15,17,22,26,1,1,1,1,1,13,13,11,1,1,1,1,5,10,
         1,1,1,15,1,5,1,1,1,22,1,15,11,1,1,1,13,1,1,13,1,23,1,1,6,1,6,1,1,19,1,
         17,1,13,1,22,1,1,1,1,13,6,1,1,1,19,7,1,23,1,1,21,1,1,6,1,3,29,21,15,1,1,
         1,1,1,1,1,14,13,1,1,1,1,1,1,1,1,1,2,10,21,11,17,23,30,1,30,3,11,1,1,1,1,
         22,2,1,1,11,6,23,3,1,1,1,1,1,1,1,1,1,23,1,23,21,3,19,1,1,26,30,1,1,1,30,
         1,1,1,5,1,1,1,1,29,1,7,1,1,2,1,30,7,17,7,13,1,1,29,1,1,1,1,26,1,1,6,13,
         1,1,1,11,1,30,1,14,11,30,1,1,1,1,1,14,1,26,6,26,1,7,23,1,11,13,2,23,1,7,
         22,1,1,1,5,22,15,1,11,1,21,1,1,13,26,30,1,22,1,1,14,29,1,1,1,1,1,30,2,1,
         1,29,1,1,3,21,11,1,3,22,5,6,10,1,1,1,1,26,11,1,22,14,1,14,1,21,1,10,23,1,
         13,1,29,19,1,14,1,22,1,1,1,1,29,29,3,1,1,19,10,5,1,1,1,22,1,1,14,2,1,1,1]

    print (s.numberOfGoodSubsets(ns))


