import dataclasses
from collections import defaultdict
from itertools import product
USED_SYMBOL = "."


@dataclasses.dataclass
class Node:
    children: dict[str: 'Node'] = dataclasses.field(default_factory=dict)
    word:  str = dataclasses.field(default=None)


class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        node = self.root
        for char in word:
            node = node.children.setdefault(char, Node())
        node.word = word

    def delete(self, word_to_delete):
        def _delete(node, word, d):
            """Clear the node corresponding to word[d],
             delete the child word[d+1] if that subtrie is completely empty,
             and return whether `node` has been cleared."""
            if d == len(word):
                node.word = None
            else:
                c = word[d]
                if c in node.children and _delete(node.children[c], word, d+1):
                    del node.children[c]
            # Return whether the subtrie rooted at node is now completely empty
            return node.word is None and len(node.children) == 0

        return _delete(self.root, word_to_delete, 0)


def build_trie(words: list[str]):
    trie = Trie()
    for word in words:
        trie.insert(word)
    return trie


def build_neighbours(width, depth):
    neighbours = defaultdict(list)
    for row, column in product(range(depth), range(width)):
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if 0 <= row+dr < depth and 0 <= column+dc < width:
                neighbours[row, column].append((row+dr, column+dc))
    return neighbours


class Solution:
    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:

        trie = build_trie(words)
        width, depth = len(board[0]), len(board)
        neighbours = build_neighbours(width, depth)
        results = []

        def dfs(row, column, node):
            if board[row][column] not in node.children:
                return

            letter = board[row][column]
            board[row][column] = USED_SYMBOL
            new_node = node.children[letter]

            if new_node.word is not None:
                results.append(new_node.word)
                trie.delete(new_node.word)
                # or delete "in place":
                # if not new_node.children:
                #     node.children.pop(letter)

            for new_row, new_column in neighbours[row, column]:
                dfs(new_row, new_column, new_node)

            # clean-up
            board[row][column] = letter

        for row_start, column_start in product(range(depth), range(width)):
            dfs(row_start, column_start, trie.root)

        return results


if __name__ == "__main__":
    solution = Solution()

    # Some LeetCode test cases.

    test_board = [["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"],
                  ["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"],
                  ["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"],
                  ["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"],
                  ["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"],
                  ["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"],
                  ["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"],
                  ["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"],
                  ["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"],
                  ["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"],
                  ["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"],
                  ["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a"]]
    # Medium.
    test_words = ["a", "aa", "aaa", "aaaa", "aaaaa", "aaaaaa", "aaaaaaa",
                  "aaaaaaaa", "aaaaaaaaa", "aaaaaaaaaa"]
    found = solution.findWords(test_board, test_words)
    print(found)
    # More words.
    with open('test/test_words_0.txt') as f:
        test_data = str.split(f.read(), ",")
    test_words = [word[1:-1] for word in test_data]
    found = solution.findWords(test_board, test_words)
    print(found)

    # Many more words.
    test_board = [["b", "a", "b", "a", "b", "a", "b", "a", "b", "a"],
                  ["a", "b", "a", "b", "a", "b", "a", "b", "a", "b"],
                  ["b", "a", "b", "a", "b", "a", "b", "a", "b", "a"],
                  ["a", "b", "a", "b", "a", "b", "a", "b", "a", "b"],
                  ["b", "a", "b", "a", "b", "a", "b", "a", "b", "a"],
                  ["a", "b", "a", "b", "a", "b", "a", "b", "a", "b"],
                  ["b", "a", "b", "a", "b", "a", "b", "a", "b", "a"],
                  ["a", "b", "a", "b", "a", "b", "a", "b", "a", "b"],
                  ["b", "a", "b", "a", "b", "a", "b", "a", "b", "a"],
                  ["a", "b", "a", "b", "a", "b", "a", "b", "a", "b"]]
    with open('test/test_words_1.txt') as f:
        test_data = str.split(f.read(), ",")
    test_words = [word[1:-1] for word in test_data]
    found = solution.findWords(test_board, test_words)
    print(found)
