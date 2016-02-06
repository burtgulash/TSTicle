#!/usr/bin/python3

from tsticle import *

if __name__ == "__main__":
    t = TST()
    #t = CompressedTST()

    words = ["autobus", "auto", "a", "kokotko", "autobusak",
            "kkt", "kokot", "kk", "k",
            "karel", "kamil", "kure",
            "kral", "kralovec", "karlovec", "kokorin", "karlstejn"]

    print("INSERTING")
    for w in words:
        t.insert(w)
        print("inserted", w)
        assert t.find(w)



    print(t)
    print("FULL SIZE:", len(t))

    for w in words:
        t.remove(w)
        print("removed", w)
        #print(t)
        print("SIZE:", len(t))

    print(t)
    print()
