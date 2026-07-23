"""Held-Karp exact travelling salesman via dynamic programming over subsets.

The travelling salesman problem asks for the shortest closed tour visiting
every city exactly once. Brute force over all (n-1)! orderings is hopeless past
a dozen cities. Held-Karp trades that factorial for an exponential that is far
smaller: the state is dp[mask][j], the length of the cheapest path that starts
at city 0, visits exactly the set of cities in mask, and currently sits at city
j. A path reaching j came from some earlier city i in mask, so
dp[mask][j] = min over i of dp[mask without j][i] + dist[i][j].

Once every full-set state is known, the answer closes the loop back to 0:
min over j of dp[full][j] + dist[j][0]. Remembering which i achieved each
minimum lets us walk the parent pointers backwards to rebuild the tour.

Complexity: O(2**n * n**2) time and O(2**n * n) space, good to roughly n = 18.
"""

from itertools import permutations

INF = float("inf")

Matrix = list[list[float]]


def held_karp(dist: Matrix) -> tuple[float, list[int]]:
    """Return the optimal tour cost and the visiting order starting at 0."""
    n = len(dist)
    if n <= 1:
        return 0.0, list(range(n))
    full = 1 << n
    dp = [[INF] * n for _ in range(full)]
    parent = [[-1] * n for _ in range(full)]
    dp[1][0] = 0.0  # start at city 0, only city 0 visited

    for mask in range(full):
        if not (mask & 1):
            continue  # every path must include the start city
        for j in range(n):
            if dp[mask][j] == INF:
                continue
            for k in range(1, n):
                if mask & (1 << k):
                    continue
                nxt = mask | (1 << k)
                cand = dp[mask][j] + dist[j][k]
                if cand < dp[nxt][k]:
                    dp[nxt][k] = cand
                    parent[nxt][k] = j

    best, last = INF, -1
    for j in range(1, n):
        cand = dp[full - 1][j] + dist[j][0]
        if cand < best:
            best, last = cand, j
    if last == -1:  # n == 1 handled above; guards a fully disconnected graph
        return INF, []

    tour = [0]
    mask, j = full - 1, last
    while j != 0:
        tour.append(j)
        pj = parent[mask][j]
        mask ^= 1 << j
        j = pj
    tour.reverse()
    return best, tour


def brute_force(dist: Matrix) -> float:
    """Exhaustive check over all orderings, only viable for tiny n."""
    n = len(dist)
    best = INF
    for perm in permutations(range(1, n)):
        order = (0,) + perm
        cost = sum(dist[order[i]][order[i + 1]] for i in range(n - 1))
        cost += dist[order[-1]][0]
        best = min(best, cost)
    return best


def tour_cost(dist: Matrix, tour: list[int]) -> float:
    n = len(tour)
    return sum(dist[tour[i]][tour[(i + 1) % n]] for i in range(n))


def main() -> None:
    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]
    cost, tour = held_karp(dist)
    print(f"4 cities: optimal cost {cost} via tour {tour}")
    print(f"  reconstructed tour cost checks: {tour_cost(dist, tour)}")
    print(f"  brute force agrees: {brute_force(dist)}")

    import random
    random.seed(7)
    for n in range(2, 9):
        pts = [(random.uniform(0, 100), random.uniform(0, 100))
               for _ in range(n)]
        d = [[((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
              for b in pts] for a in pts]
        hk, tour = held_karp(d)
        bf = brute_force(d)
        assert abs(hk - bf) < 1e-9, (n, hk, bf)
        assert abs(tour_cost(d, tour) - hk) < 1e-9
    print("random cross-checks n=2..8: held-karp == brute force")

    print("\nedge cases:")
    print("  one city:", held_karp([[0]]))
    print("  two cities:", held_karp([[0, 5], [5, 0]]))


if __name__ == "__main__":
    main()
