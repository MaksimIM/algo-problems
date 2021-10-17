# We maintain a stack of active rectangles.
# One could store them as pairs (start, height)
# Here an optimization is to store rightmost locations of bottleneck heights.
# Then both start and height are encoded in same queue:
# the height is just heights[bottleneck location],
# and the start of the rectangle is just after
# the location of the rightmost bottleneck
# for the next shorter rectangle in the queue!

class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        heights.append(0)
        rightmost_locations_of_bottleneck = [-1]
        max_area = 0

        for end, next_height in enumerate(heights):

            # Close off non-extendable rectangles.
            while next_height < heights[rightmost_locations_of_bottleneck[-1]]:
                # Remove and compute height.
                height = heights[rightmost_locations_of_bottleneck.pop()]
                area = (end-(rightmost_locations_of_bottleneck[-1]+1))*height
                if area > max_area:
                    max_area = area

            # If needed, move the bottleneck.
            if next_height == heights[rightmost_locations_of_bottleneck[-1]]:
                rightmost_locations_of_bottleneck[-1] = end
            # If needed, add a new rectangle.
            else:
                rightmost_locations_of_bottleneck.append(end)

        return max_area


if __name__ == "__main__":
    solution = Solution()
    heights = [2]
    found = solution.largestRectangleArea(heights)
    print(found)
