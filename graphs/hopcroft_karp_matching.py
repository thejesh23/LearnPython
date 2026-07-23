"""Hopcroft-Karp: maximum bipartite matching in O(E * sqrt(V)).

A matching pairs left vertices with right vertices so no vertex is used twice; a
maximum matching pairs as many as possible. The simple Kuhn/Hungarian method
grows one augmenting path at a time — a path that alternates unmatched and
matched edges and starts and ends free — flipping it to gain one pair, for O(VE)
overall.

Hopcroft-Karp augments in phases. Each phase runs a BFS that layers the free
left vertices by shortest alternating distance, then a DFS that greedily flips a
maximal set of vertex-disjoint shortest augmenting paths at once. Because the
shortest augmenting-path length strictly increases every phase and only
O(sqrt(V)) distinct lengths can occur before the matching is maximum, just
O(sqrt(V)) phases are needed, each costing O(E) — hence O(E * sqrt(V)).

The correctness rests on Berge's theorem: a matching is maximum exactly when no
augmenting path remains. Attacking the shortest ones in disjoint batches is what
turns Kuhn's per-path grind into a per-batch sprint.
"""

from collections import deque

INF = float("inf")


def hopcroft_karp(
    adj: dict[int, list[int]], left: list[int], right: list[int]
) -> dict[int, int]:
    """Return a maximum matching as {left_vertex: right_vertex}."""
    match_l: dict[int, int | None] = {u: None for u in left}
    match_r: dict[int, int | None] = {v: None for v in right}
    dist: dict[int, float] = {}

    def bfs() -> bool:
        queue: deque[int] = deque()
        for u in left:
            if match_l[u] is None:
                dist[u] = 0
                queue.append(u)
            else:
                dist[u] = INF
        found = False
        while queue:
            u = queue.popleft()
            for v in adj.get(u, []):
                w = match_r[v]  # left vertex currently holding v, if any
                if w is None:
                    found = True  # reached a free right vertex: path exists
                elif dist[w] == INF:
                    dist[w] = dist[u] + 1
                    queue.append(w)
        return found

    def dfs(u: int) -> bool:
        for v in adj.get(u, []):
            w = match_r[v]
            if w is None or (dist[w] == dist[u] + 1 and dfs(w)):
                match_l[u] = v
                match_r[v] = u
                return True
        dist[u] = INF  # dead end this phase; do not revisit
        return False

    while bfs():
        for u in left:
            if match_l[u] is None:
                dfs(u)

    return {u: v for u, v in match_l.items() if v is not None}


def main() -> None:
    # Left {0,1,2,3} applicants, right {10,11,12,13} jobs.
    adj = {
        0: [10, 11],
        1: [10, 12],
        2: [11, 13],
        3: [12],
    }
    left = [0, 1, 2, 3]
    right = [10, 11, 12, 13]

    matching = hopcroft_karp(adj, left, right)
    print(f"matching: {dict(sorted(matching.items()))}")
    print(f"matched pairs: {len(matching)}")

    # Every left vertex here can be matched: a perfect matching of size 4.
    assert len(matching) == 4

    # No right vertex used twice, and every pair is a real edge.
    used_right = list(matching.values())
    assert len(used_right) == len(set(used_right))
    assert all(v in adj[u] for u, v in matching.items())
    print("validity checks passed")

    # Edge case: two left vertices compete for the only job -> size 1.
    tight = {0: [10], 1: [10]}
    m2 = hopcroft_karp(tight, [0, 1], [10])
    print(f"contested single job: {m2} (size {len(m2)})")

    # Edge case: an isolated left vertex stays unmatched.
    sparse = {0: [10], 1: []}
    m3 = hopcroft_karp(sparse, [0, 1], [10])
    print(f"isolated vertex: {m3} (size {len(m3)})")


if __name__ == "__main__":
    main()
