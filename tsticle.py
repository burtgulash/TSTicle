#!/usr/bin/python3


class TNode:

    def __init__(self, label):
        self.label = label
        self.left = None
        self.mid = None
        self.right = None


class TST:

    def __init__(self):
        self.size = 0
        self.root = None

    def __len__(self):
        return self.size

    def find(self, word):
        word += '\0'
        cur = self.root
        i = 0

        while cur is not None:
            prev = cur
            if word[i] < cur.label:
                cur = cur.left
            elif word[i] > cur.label:
                cur = cur.right
            else:
                if i == len(word) - 1:
                    return True
                cur = cur.mid
                i += 1

        return False

    def insert(self, word):
        word += '\0'
        prev = cur = self.root
        i = 0

        while cur is not None:
            prev = cur
            if word[i] < cur.label:
                cur = cur.left
            elif word[i] > cur.label:
                cur = cur.right
            else:
                if i == len(word) - 1:
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
            if word[i] < prev.label:
                prev.left = cur
            elif word[i] > prev.label:
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

    def __str__(self):
        s = []
        def _str(n, acc, lvl, direction):
            prepend = lvl * "  "
            if n is None:
                if direction == "-":
                    s.append(prepend + ">> {"+acc+"}")
                return

            s.append(prepend + direction + " " + n.label)
            _str(n.right, acc, lvl + 1, "/")
            _str(n.mid, acc + n.label, lvl + 1, "-")
            _str(n.left, acc, lvl + 1, "\\")


        _str(self.root, "", 0, "-")

        return "\n".join(s).replace('\0', '$')


class CompressedTST:

    def __init__(self):
        self.size = 0
        self.root = None

    def __len__(self):
        return self.size

    def find(self, word):
        word += '\0'
        cur = self.root
        i = 0

        while cur is not None:
            j = 0
            while j < len(cur.label) - 1:
                if word[i + j] != cur.label[j]:
                    return False
                j += 1

            i += j
            if word[i] < cur.label[j]:
                cur = cur.left
            elif word[i] > cur.label[j]:
                cur = cur.right
            else:
                if i == len(word) - 1:
                    return True
                cur = cur.mid
                i += 1

        return False

    def insert(self, word):
        word += '\0'
        prev = cur = self.root
        c = None
        i = 0

        break_inner = False
        while i < len(word) and cur is not None:
            prev = cur
            j = 0
            while j < len(cur.label) - 1:
                c = cur.label[j]
                if word[i + j] != c:
                    common_prefix = cur.label[:j + 1]
                    label_suffix = cur.label[j + 1:]

                    new = TNode(label_suffix)
                    new.left = cur.left
                    new.mid = cur.mid
                    new.right = cur.right

                    cur.label = common_prefix
                    cur.left = None
                    cur.mid = new
                    cur.right = None

                    break_inner = True
                    break
                j += 1

            i += j
            if break_inner:
                break

            c = cur.label[j]
            if word[i] < c:
                cur = cur.left
            elif word[i] > c:
                cur = cur.right
            else:
                if i == len(word) - 1:
                    return True
                cur = cur.mid
                i += 1

        # create first node of subtree
        cur = TNode(word[i:])

        # if root is empty, put subtree as root
        if prev is None:
            self.root = cur
        else:
            # find in which direction we should put the newly created subtree
            if word[i] < c:
                prev.left = cur
            elif word[i] > c:
                prev.right = cur
            else:
                prev.mid = cur

        # increase size of the tree
        self.size += 1

    def __str__(self):
        s = []
        def _str(n, acc, lvl, direction):
            prepend = lvl * "  "
            if n is None:
                if direction == "-":
                    s.append(prepend + ">> {"+acc+"}")
                return

            s.append(prepend + direction + " " + n.label)
            _str(n.right, acc + n.label[:-1], lvl + 1, "/")
            _str(n.mid, acc + n.label, lvl + 1, "-")
            _str(n.left, acc + n.label[:-1], lvl + 1, "\\")


        _str(self.root, "", 0, "-")

        return "\n".join(s).replace('\0', '$')



if __name__ == "__main__":
    #t = TST()
    t = CompressedTST()

    words = ["autobus", "auto", "a", "kokotko", "autobusak",
            "kkt", "kokot", "kk", "k",
            "karel", "kamil", "kure",
            "kral", "kralovec", "karlovec", "kokorin", "karlstejn"]

    for w in words:
        t.insert(w)
        assert t.find(w)

    print(t)
    print()
