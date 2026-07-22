"""Floyd-Warshall: shortest paths between every pair of nodes at once.

Instead of running a single-source algorithm V times, this fills in a V x V
distance matrix directly. The trick is the loop order. The outer loop picks a
node k and asks, for every pair (i, j), whether routing through k is cheaper
than the best route found so far.

Read the outer loop as a growing permission list: after k rounds the matrix
holds the shortest path from i to j that is allowed to use only the first k
nodes as intermediates. Once every node has had its turn, the restriction is
gone and the matrix is exact. That is why k must be the outermost loop —
swapping it inside gives wrong answers.

Negative edges are fine; negative cycles are not, and they show up as a
negative value on the diagonal. Storing a next-hop matrix alongside the
distances lets you rebuild the actual route.

Complexity: O(V^3) time and O(V^2) space, with a tight inner loop that often
beats V runs of Dijkstra on small dense graphs.
"""

INF = float("inf")


def floyd_warshall(
    weights: list[list[float]],
) -> tuple[list[list[float]], list[list[int | None]]]:
    """Take an adjacency matrix (INF where there is no edge); return dist and next-hop."""
    n = len(weights)
    dist = [row[:] for row in weights]
    nxt: list[list[int | None]] = [
        [j if i != j and weights[i][j] != INF else None for j in range(n)]
        for i in range(n)
    ]
    for i in range(n):
        dist[i][i] = min(dist[i][i], 0.0)

    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue  # no route into k, so k cannot help any j
            for j in range(n):
                through = dist[i][k] + dist[k][j]
                if through < dist[i][j]:
                    dist[i][j] = through
                    nxt[i][j] = nxt[i][k]
    return dist, nxt


def has_negative_cycle(dist: list[list[float]]) -> bool:
    """A node cheaper than zero to return to sits on a negative cycle."""
    return any(dist[i][i] < 0 for i in range(len(dist)))


def path(nxt: list[list[int | None]], start: int, goal: int) -> list[int] | None:
    if nxt[start][goal] is None and start != goal:
        return None
    route = [start]
    node = start
    while node != goal:
        node = nxt[node][goal]  # type: ignore[assignment]
        route.append(node)
    return route


def main() -> None:
    names = ["A", "B", "C", "D"]
    #  A -3-> B -2-> C -1-> D,  plus A -8-> C and D -2-> A
    weights: list[list[float]] = [
        [0, 3, 8, INF],
        [INF, 0, 2, INF],
        [INF, INF, 0, 1],
        [2, INF, INF, 0],
    ]

    dist, nxt = floyd_warshall(weights)
    header = "     " + "".join(f"{n:>6}" for n in names)
    print(header)
    for i, row in enumerate(dist):
        cells = "".join(f"{v:>6g}" if v != INF else f"{'inf':>6}" for v in row)
        print(f"{names[i]:>5}{cells}")

    # A -> C costs 5 via B, beating the direct 8-weight edge.
    print(f"A -> C: {[names[i] for i in path(nxt, 0, 2)]}")
    print(f"B -> A: {[names[i] for i in path(nxt, 1, 0)]}")
    print(f"A -> A: {[names[i] for i in path(nxt, 0, 0)]}")
    print(f"negative cycle: {has_negative_cycle(dist)}")

    # Edge case: a node nothing can reach keeps an infinite column.
    isolated: list[list[float]] = [[0, 1, INF], [1, 0, INF], [INF, INF, 0]]
    d2, n2 = floyd_warshall(isolated)
    print(f"unreachable pair 0 -> 2: {d2[0][2]}, path {path(n2, 0, 2)}")

    # Edge case: the cycle 0 -> 1 -> 0 has total weight -1.
    negative: list[list[float]] = [[0, 1, INF], [-2, 0, INF], [INF, INF, 0]]
    d3, _ = floyd_warshall(negative)
    print(f"negative cycle detected: {has_negative_cycle(d3)}")


if __name__ == "__main__":
    main()
