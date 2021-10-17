# For each rectangle, some bar is the bottleneck.
# So we find for each bar the rectangle in which it is a bottleneck, and take the max area.
# To do this, find how far the bar can extend to the left, then how far to the right. Both of those are done via dynamic programming.
class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        l = len(heights)

        left_edge = [0]*l
        for i, height in enumerate(heights):
            current_left_edge = i
            while current_left_edge > 0 and heights[current_left_edge-1] >= height:
                current_left_edge = left_edge[current_left_edge-1]
            left_edge[i] = current_left_edge

        right_edge = [0]*l
        for i, height in enumerate(reversed(heights)):
            current_right_edge = i
            while current_right_edge > 0 and heights[l-1-(current_right_edge-1)] >= height:
                current_right_edge = right_edge[current_right_edge-1]
            right_edge[i] = current_right_edge

        return max(height*((l-1-right_edge[l-1-i])-left_edge[i]+1) for i, height in enumerate(heights))


if __name__ == "__main__":
    solution = Solution()
    heights = [2, 1, 5, 6, 2, 3]
    found = solution.largestRectangleArea(heights)
    print(found)
