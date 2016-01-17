#!/usr/bin/python3


class TNode:

    def __init__(self, c):
        self.c = c
        self.left = None
        self.mid = None
        self.right = None

class TernaryTrie:

    def __init__(self):
        self.size = 0
        self.root = None

    def __len__(self):
        return self.size

    def find(self, word):
        cur = self.root
        i = 0

        while i < len(word) and cur is not None:
            if word[i] < cur.c:
                cur = cur.left
            elif word[i] > cur.c:
                cur = cur.right
            else:
                if i == len(word) - 1:
                    return True

                cur = cur.mid
                i += 1

        return False

    def insert(self, word):
        prev = cur = self.root
        i = 0

        while cur is not None:
            prev = cur
            if word[i] < cur.c:
                cur = cur.left
            elif word[i] > cur.c:
                cur = cur.right
            else:
                if i == len(word) - 1:
                    # word present in trie
                    return

                cur = cur.mid
                i += 1

        # create first node of subtree
        cur = TNode(word[i])

        # if root is empty, put subtree as root
        if prev is None:
            self.root = cur
        else:
            # find in which direction we should put the newly created subtree
            if word[i] < prev.c:
                prev.left = cur
            elif word[i] > prev.c:
                prev.right = cur
            else:
                prev.mid = cur
        i += 1

        # create subtree of word suffix that was not found in the tree
        while i < len(word):
            cur.mid = TNode(word[i])
            cur = cur.mid
            i += 1

        # increase size of the tree
        self.size += 1


if __name__ == "__main__":
    t = TernaryTrie()
    words = "autobus", "auto", "a", "kokotko", "autobusak", "kkt", "kokot", "kk", "k"
    for w in words:
        t.insert(w)
        print(t.find(w), w)
