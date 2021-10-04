class Solution:
    def isSelfCrossing(self, distance: list[int]) -> bool:
        for i in range(len(distance)-2):
            if distance[i+2] <= distance[i]:
                I = i
                break
        else:
            return False

        for i in range(I+1, len(distance)-2):
            if distance[i+2] >= distance[i]:
                return True

        # Check s(I-2) and s(I+3)
        ls = [0]*6
        for j in range(-2, 4):
            if len(distance)-1 >= I+j >= 0:
                ls[j+2] = distance[I+j]
        return ls[0]+ls[4] >= ls[2] and ls[1]+ls[5] >= ls[3]
