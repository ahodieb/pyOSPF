# graph implementation using Dictionaries insted of two dimentional arrays


def dijkestra(G, O):
    S = [O]  # shoretes path nodes
    V = G.keys()  # Vertices
    V.remove(O)

    d = {O: 0}  # distance from orign to node
    E = {}  # un optimized routing table . need to adjuest gatways

    dp = {}  # d prime
    Ep = {}

    n_s = O  # newly added s
    for v in V:
        dp[v] = G[O][v]
        Ep[v] = (v, O)

    while (V):
        for v in V:
        # causes quadratic time atleast
        # i already cash the results in the above variables but i cant get
        # my mind around that idea for now .
            # for s in S:
            #     if d[s] + G[s][v] < dp[v]:
            #         dp[v] = d[s] + G[s][v]
            #         Ep[v] = (v, s)

            if d[n_s] + G[n_s][v] < dp[v]:
                dp[v] = d[n_s] + G[n_s][v]
                Ep[v] = (v, n_s)

        m = min(dp, key=dp.get)

        V.remove(m)
        S.append(m)
        n_s = m

        d[m] = (dp[m])
        dp.pop(m)

        E[m] = (Ep[m])
        Ep.pop(m)

    d.pop(O)
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
        1: {1: 0,   2: 4,   3: 6,   4: 8,   5: inf, 6: inf, 7: inf},
        2: {1: inf, 2: 0,   3: 1,   4: inf, 5: 7,   6: inf, 7: inf},
        3: {1: inf, 2: inf, 3: 0,   4: 2,   5: 5,   6: 4,   7: inf},
        4: {1: inf, 2: inf, 3: inf, 4: 0,   5: inf, 6: 5,   7: inf},
        5: {1: inf, 2: inf, 3: inf, 4: inf, 5: 0,   6: inf, 7: 6},
        6: {1: inf, 2: inf, 3: inf, 4: inf, 5: 1,   6: inf, 7: inf},
        7: {1: inf, 2: inf, 3: inf, 4: inf, 5: inf, 6: inf, 7: 0},
    }

    G = {
        'r4': {'r4': 0, 'r5': inf, 'r1': inf, 'r2': 10, 'r3': 25},
        'r5': {'r4': inf, 'r5': 0, 'r1': inf, 'r2': 10, 'r3': inf},
        'r1': {'r4': inf, 'r5': inf, 'r1': 0, 'r2': 100, 'r3': 100},
        'r2': {'r4': 10, 'r5': 10, 'r1': 100, 'r2': 0, 'r3': 50},
        'r3': {'r4': 25, 'r5': inf, 'r1': 100, 'r2': 50, 'r3': 0}
    }

    d, E = dijkestra(G, 'r5')
    print d
    print E

if __name__ == '__main__':
    main()
