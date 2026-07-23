"""Bipartite test by 2-coloring, with an odd-cycle witness when it fails.

A graph is bipartite exactly when its vertices split into two groups with every
edge crossing between them — equivalently, when it can be 2-colored so no edge
joins same-colored endpoints. BFS colors greedily: give the start color 0, then
color each neighbour with the opposite of the current node. If BFS ever meets an
already-colored neighbour wearing the same color, the graph is not bipartite.

That conflict is not just a failure flag; it pinpoints an odd cycle. Tracing
parent pointers back from the two same-colored endpoints to their common
ancestor yields a closed walk of odd length, the classic certificate that
bipartiteness is impossible. A well-known consequence (Koenig's theorem) is that
in a bipartite graph the size of a maximum matching equals the size of a minimum
vertex cover, which is why bipartite structure is worth detecting. The check
runs in O(V + E) over each connected component.
"""

from collections import deque


def two_color(n: int,
              adj: list[list[int]]) -> tuple[list[int] | None, list[int]]:
    """Return (coloring, odd_cycle). If bipartite, odd_cycle is empty and
    coloring holds 0/1 per node; otherwise coloring is None."""
    color = [-1] * n
    parent = [-1] * n
    for start in range(n):
        if color[start] != -1:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    parent[v] = u
                    queue.append(v)
                elif color[v] == color[u]:
                    return None, _odd_cycle(u, v, parent)
    return color, []


def _odd_cycle(u: int, v: int, parent: list[int]) -> list[int]:
    """Build an odd cycle from the conflicting edge (u, v)."""
    # Climb both ends to equal depth, then together, to the common ancestor.
    path_u, path_v = [], []
    a, b = u, v
    du = _depth(a, parent)
    dv = _depth(b, parent)
    while du > dv:
        path_u.append(a)
        a = parent[a]
        du -= 1
    while dv > du:
        path_v.append(b)
        b = parent[b]
        dv -= 1
    while a != b:
        path_u.append(a)
        path_v.append(b)
        a = parent[a]
        b = parent[b]
    lca = a
    cycle = path_u + [lca] + path_v[::-1]
    return cycle


def _depth(node: int, parent: list[int]) -> int:
    d = 0
    while parent[node] != -1:
        node = parent[node]
        d += 1
    return d


def _is_odd_cycle(cycle: list[int], adj: list[list[int]]) -> bool:
    if len(cycle) % 2 == 0 or len(cycle) < 3:
        return False
    m = len(cycle)
    return all(cycle[(i + 1) % m] in adj[cycle[i]] for i in range(m))


def main() -> None:
    # Bipartite: a 6-cycle splits cleanly into two color classes.
    n = 6
    even_cycle: list[list[int]] = [[] for _ in range(n)]
    for a, b in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]:
        even_cycle[a].append(b)
        even_cycle[b].append(a)
    color, odd = two_color(n, even_cycle)
    print(f"6-cycle coloring: {color}")
    assert color is not None and odd == []
    for a in range(n):
        for b in even_cycle[a]:
            assert color[a] != color[b], "edge must cross color classes"

    # Not bipartite: a triangle forces two neighbours to share a color.
    tri: list[list[int]] = [[] for _ in range(3)]
    for a, b in [(0, 1), (1, 2), (2, 0)]:
        tri[a].append(b)
        tri[b].append(a)
    color, odd = two_color(3, tri)
    print(f"triangle coloring: {color}, odd cycle witness: {odd}")
    assert color is None
    assert _is_odd_cycle(odd, tri), "witness must be a real odd cycle"

    # Edge case: two disconnected edges are trivially bipartite.
    forest: list[list[int]] = [[1], [0], [3], [2]]
    color, odd = two_color(4, forest)
    print(f"two-edge forest coloring: {color}")
    assert color is not None

    print("all cross-checks passed")


if __name__ == "__main__":
    main()
