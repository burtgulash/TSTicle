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

    def remove(self, word):
        word += '\0'
        last_fork = prev = cur = self.root
        i = 0

        LEFT = 1
        MID = 2
        RIGHT = 3

        turn = None
        while cur is not None:
            is_fork = False

            if cur.left is not None or cur.right is not None:
                last_fork = cur
                is_fork = True


            if word[i] < cur.label:
                prev = cur
                cur = cur.left
                turn = LEFT
            elif word[i] > cur.label:
                prev = cur
                cur = cur.right
                turn = RIGHT
            else:
                if i == len(word) - 1:
                    assert cur.left is None
                    if cur.right is None:
                        if turn is None:
                            self.root = None
                        elif turn is LEFT:
                            last_fork.left = None
                        elif turn is RIGHT:
                            last_fork.right = None
                        else:
                            assert turn is MID
                            if last_fork.right is not None:
                                last_fork.label = last_fork.right.label
                                last_fork.mid = last_fork.right.mid

                                cur = last_fork
                                if cur.left is None:
                                    cur.left = last_fork.right.left
                                else:
                                    cur = cur.left
                                    while cur.right is not None:
                                        cur = cur.right
                                    cur.right = last_fork.right.left
                                last_fork.right = None

                            elif last_fork.left is not None:
                                last_fork.label = last_fork.left.label
                                last_fork.mid = last_fork.left.mid

                                cur = last_fork
                                if cur.right is None:
                                    cur.right = last_fork.left.right
                                else:
                                    cur = cur.right
                                    while cur.left is not None:
                                        cur = cur.left
                                    cur.left = last_fork.left.right
                                last_fork.left = None

                            else:
                                raise AssertionError("fork node must have either left or right subnode!")
                    else:
                        prev.mid = cur.right

                    return True

                if is_fork:
                    turn = MID

                prev = cur
                cur = cur.mid
                i += 1

        return False


    def find(self, word):
        word += '\0'
        cur = self.root
        i = 0

        while cur is not None:
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

    def descendants(self, prefix):
        def _d(tnode, acc):
            if acc and acc[-1] == '\0':
                yield acc[:-1]
            if tnode is None:
                return
            yield from _d(tnode.left, acc)
            yield from _d(tnode.mid, acc + tnode.label)
            yield from _d(tnode.right, acc)

        cur = self.root
        i = 0

        while i < len(prefix) and cur is not None:
            if prefix[i] < cur.label:
                cur = cur.left
            elif prefix[i] > cur.label:
                cur = cur.right
            else:
                cur = cur.mid
                if i == len(prefix) - 1:
                    yield from _d(cur, prefix)
                i += 1

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

    def remove(self, word):
        raise NotImplementedError("Remove not implemented yet")

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

    def descendants(self, prefix):
        def _d(tnode, acc):
            if acc and acc[-1] == '\0':
                yield acc[:-1]
            if tnode is None:
                return
            yield from _d(tnode.left, acc + tnode.label[:-1])
            yield from _d(tnode.mid, acc + tnode.label)
            yield from _d(tnode.right, acc + tnode.label[:-1])

        cur = self.root
        i = 0

        while i < len(prefix) and cur is not None:
            j = 0
            while j < len(cur.label) - 1:
                if i + j == len(prefix) - 1:
                    yield from _d(cur, prefix[:i])
                    return
                if prefix[i + j] != cur.label[j]:
                    return
                j += 1

            i += j
            if prefix[i] < cur.label[j]:
                cur = cur.left
            elif prefix[i] > cur.label[j]:
                cur = cur.right
            else:
                cur = cur.mid
                if i == len(prefix) - 1:
                    yield from _d(cur, prefix)
                    return
                i += 1

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
    t = TST()
    #t = CompressedTST()

    words = ["autobus", "auto", "a", "kokotko", "autobusak",
            "kkt", "kokot", "kk", "k",
            "karel", "kamil", "kure",
            "kral", "kralovec", "karlovec", "kokorin", "karlstejn"]

    #words = ["autobus", "autor", "auto", "automat", "automaton", "authorka"]
    words = ["auto", "automat", "automaton"]

    for w in words:
        t.insert(w)
        assert t.find(w)



    print(t)
    print()

    #t.remove("auto")
    #t.remove("automaton")
    #t.remove("autobus")

    print(t)
    print()
