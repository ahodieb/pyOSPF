# graph implementation using Dictionaries insted of two dimentional arrays


def dijkestra(G, O):
    S = [O]  # shoretes path nodes
    V = G.keys()  # Vertices
    V.remove(O)
    d = {O: 0}  # distance
    E = {}  # un optimized routing table . need to adjuest gatways

    dp = {}  # d prime
    Ep = {}
    for v in V:
        dp[v] = G[O][v]
        Ep[v] = (v, O)

    while (V):

        for v in V:
        # this loop is ineffecient try to optimise later (23/4/2013)
        # causes quadratic time atleast
        # i already cash the results in the above variables but i cant get
        # my mind around that idea for now .
            for s in S:
                print "current s : ", s
                print "current v", v
                print "g[s][v] :", G[s][v]
                print "dp[v", dp[v]

                if d[s] + G[s][v] < dp[v]:
                    dp[v] = d[s] + G[s][v]
                    Ep[v] = (v, s)

        m = min(dp)

        V.remove(m)
        S.append(m)

        d[m] = (dp[m])
        dp.pop(m)

        E[m] = (Ep[m])
        Ep.pop(m)

    return (d, E)


def main():
    # Sample Graph

# """

#                           +--------------7---------------+
#                           |                              |
#                           |                              |
#                        +--+--+                        +--v--+
#                        |     |                        |     |
#         +------4------->  2  |                        |  5  +-----6------+
#         |              |     |             +---------->     |            |
#         |              +--+--+             |          +--^--+            |
#         |                 |                |             |               |
#         |                 1                5             |               |
#         |                 |                |             |               |
#      +--+--+           +--v--+             |             |            +--v--+
#      |     |           |     +-------------+             |            |     |
#      |  1  +-----6----->  3  +                           1            |  7  |
#      |     |           |     +-------------+             |            |     |
#      +--+--+           +--+--+             |             |            +--^--+
#         |                 |                |             |               |
#         |                 2                |             |               |
#         |                 |                4             |               |
#         |                 |                |             |               |
#         |              +--v--+             |          +--+--+            |
#         |              |     |             |          |     |            |
#         +-------8------>  4  |             +---------->  6  +------8-----+
#                        |     |                        |     |
#                        +--+--+                        +-^---+
#                           |                             |
#                           +--------------5-------------->
# """
    inf = float("inf")
    G = {
        1: {1: 0, 2: 4, 3: 6, 4: 8, 5: inf, 6: inf, 7: inf},
        2: {1: inf, 2: 0, 3: 1, 4: inf, 5: 7, 6: inf, 7: inf},
        3: {1: inf, 2: inf, 3: 0, 4: 2, 5: 5, 6: 4, 7: inf},
        4: {1: inf, 2: inf, 3: inf, 4: 0, 5: inf, 6: 5, 7: inf},
        5: {1: inf, 2: inf, 3: inf, 4: inf, 5: 0, 6: inf, 7: 6},
        6: {1: inf, 2: inf, 3: inf, 4: inf, 5: 1, 6: inf, 7: inf},
        7: {1: inf, 2: inf, 3: inf, 4: inf, 5: inf, 6: inf, 7: inf},
    }

    d, E = dijkestra(G, 1)
    print d
    print E

if __name__ == '__main__':
    main()
