"""Johnson's algorithm: all-pairs shortest paths with negative edges allowed.

Dijkstra is fast but cannot cope with negative edge weights; Bellman-Ford copes
but is slow to run from every source. Johnson's trick gets the best of both. Add
a virtual node with a zero-weight edge to every vertex and run one Bellman-Ford
from it to get a potential h(v) — the shortest distance to each vertex. Reweight
every edge (u, v) to w(u, v) + h(u) - h(v). These reduced weights are provably
non-negative, and shortest paths are preserved because the h terms telescope
along any path.

Now Dijkstra runs correctly from each source over the reweighted graph. To
recover a true distance, undo the shift: dist(u, v) = reduced(u, v) - h(u) + h(v).
If the initial Bellman-Ford detects a negative cycle we bail out. The overall
cost is O(VE) for the reweighting plus V Dijkstras, i.e. O(VE + V E log V),
which beats Floyd-Warshall's O(V^3) on sparse graphs.
"""

import heapq

INF = float("inf")


def bellman_ford(n: int, edges: list[tuple[int, int, int]],
                 src: int) -> list[float] | None:
    """Return shortest distances from src, or None on a negative cycle."""
    dist = [INF] * n
    dist[src] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None  # negative cycle reachable
    return dist


def dijkstra(n: int, adj: list[list[tuple[int, int]]],
             src: int) -> list[float]:
    dist = [INF] * n
    dist[src] = 0
    pq: list[tuple[int, int]] = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (d + w, v))
    return dist


def johnson(n: int,
            edges: list[tuple[int, int, int]]) -> list[list[float]] | None:
    """All-pairs shortest paths, or None if a negative cycle exists."""
    # Virtual node n with a 0-weight edge to every vertex.
    augmented = edges + [(n, v, 0) for v in range(n)]
    h = bellman_ford(n + 1, augmented, n)
    if h is None:
        return None

    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, int(w + h[u] - h[v])))

    result: list[list[float]] = []
    for src in range(n):
        reduced = dijkstra(n, adj, src)
        row = [
            (reduced[v] - h[src] + h[v]) if reduced[v] != INF else INF
            for v in range(n)
        ]
        result.append(row)
    return result


def floyd_warshall(n: int,
                   edges: list[tuple[int, int, int]]) -> list[list[float]]:
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)
    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


def main() -> None:
    # 5 nodes, some negative edges but no negative cycle.
    n = 5
    edges = [
        (0, 1, 3), (0, 2, 8), (0, 4, -4), (1, 3, 1), (1, 4, 7),
        (2, 1, 4), (3, 0, 2), (3, 2, -5), (4, 3, 6),
    ]
    result = johnson(n, edges)
    assert result is not None, "graph has no negative cycle"

    reference = floyd_warshall(n, edges)
    print("all-pairs shortest paths (Johnson):")
    for i in range(n):
        row = [("inf" if x == INF else int(x)) for x in result[i]]
        print(f"  from {i}: {row}")
        assert result[i] == reference[i], "Johnson must match Floyd-Warshall"

    # Edge case: a negative cycle is detected and reported.
    cyc = [(0, 1, 1), (1, 2, -3), (2, 0, 1)]
    print(f"negative cycle detected -> {johnson(3, cyc) is None}")
    assert johnson(3, cyc) is None

    print("all cross-checks passed")


if __name__ == "__main__":
    main()
