from itertools import permutations


def operation_count(heights):
    n = len(heights)
    count = 0
    left_edge = [0]*n
    for i, height in enumerate(heights):
        current_left_edge = i
        while current_left_edge > 0 and heights[current_left_edge-1] >= height:
            current_left_edge = left_edge[current_left_edge-1]
            count += 1
        left_edge[i] = current_left_edge
    return count


if __name__ == "__main__":
    N = 4
    max_count=0
    max_perms = []
    for permutation in permutations(range(N)):
        count=operation_count(permutation)

        print(count, permutation)

        '''
        if count==max_count:
            max_perms.append(permutation)
        if count>max_count:
            max_count=count
            max_perms=[permutation]

    print(max_count, max_perms)'''

