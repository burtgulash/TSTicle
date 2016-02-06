#!/usr/bin/python3

from tsticle import *

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

    t.remove("auto")

    print(t)
    print()
