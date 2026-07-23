"""Articulation points and bridges: the single points of failure in a network.

In a connected undirected graph an articulation point (cut vertex) is a node
whose removal disconnects the graph; a bridge is an edge whose removal does the
same. Both fall out of one DFS that tracks, for each node, its discovery time
and its lowlink — the earliest discovery time reachable from its subtree using
tree edges plus at most one back-edge.

For a tree edge u-v, the subtree rooted at v can only escape upward past u if
some node in it has a back-edge to an ancestor of u. If low[v] >= disc[u] then
no such escape exists, so removing u cuts v's subtree off: u is an articulation
point. When the inequality is strict, low[v] > disc[u], the edge u-v itself is a
bridge — even a back-edge to u would not save it.

The root of the DFS tree needs a special rule: it has no ancestor to be cut
from, so it is an articulation point only when it has two or more DFS children,
meaning the tree branched and those branches meet nowhere else. Complexity is
O(V + E). This code assumes no parallel edges between the same pair.
"""

Graph = dict[str, list[str]]


def find_cut_vertices_and_bridges(
    graph: Graph,
) -> tuple[set[str], list[tuple[str, str]]]:
    disc: dict[str, int] = {}
    low: dict[str, int] = {}
    cut_vertices: set[str] = set()
    bridges: list[tuple[str, str]] = []
    timer = 0

    def dfs(node: str, parent: str | None) -> None:
        nonlocal timer
        disc[node] = low[node] = timer
        timer += 1
        children = 0
        for nxt in graph.get(node, []):
            if nxt == parent:
                continue  # do not bounce straight back along the tree edge
            if nxt in disc:
                low[node] = min(low[node], disc[nxt])  # back-edge
            else:
                children += 1
                dfs(nxt, node)
                low[node] = min(low[node], low[nxt])
                if parent is not None and low[nxt] >= disc[node]:
                    cut_vertices.add(node)
                if low[nxt] > disc[node]:
                    bridges.append((node, nxt))
        if parent is None and children > 1:
            cut_vertices.add(node)  # root special case

    for node in graph:
        if node not in disc:
            dfs(node, None)
    return cut_vertices, bridges


def main() -> None:
    #    A - B - C
    #        |   |
    #        D - E        F - G   (F-G is a separate bridge)
    graph: Graph = {
        "A": ["B"],
        "B": ["A", "C", "D"],
        "C": ["B", "E"],
        "D": ["B", "E"],
        "E": ["C", "D"],
        "F": ["G"],
        "G": ["F"],
    }

    cuts, bridges = find_cut_vertices_and_bridges(graph)
    print(f"articulation points: {sorted(cuts)}")
    print(f"bridges: {sorted(tuple(sorted(e)) for e in bridges)}")

    # Cross-check by brute force: delete each vertex/edge and recount components.
    def components(g: Graph) -> int:
        seen: set[str] = set()
        count = 0
        for start in g:
            if start in seen:
                continue
            count += 1
            stack = [start]
            while stack:
                n = stack.pop()
                if n in seen:
                    continue
                seen.add(n)
                stack.extend(m for m in g.get(n, []) if m not in seen)
        return count

    base = components(graph)

    def without_vertex(v: str) -> Graph:
        return {n: [m for m in nb if m != v] for n, nb in graph.items() if n != v}

    brute_cuts = {v for v in graph if components(without_vertex(v)) > base}
    assert brute_cuts == cuts, (brute_cuts, cuts)

    def without_edge(a: str, b: str) -> Graph:
        return {
            n: [m for m in nb if not ({n, m} == {a, b})]
            for n, nb in graph.items()
        }

    brute_bridges = {
        tuple(sorted((a, b)))
        for a in graph
        for b in graph.get(a, [])
        if components(without_edge(a, b)) > base
    }
    assert brute_bridges == {tuple(sorted(e)) for e in bridges}
    print("brute-force removal check passed")

    # Edge case: a triangle is 2-connected, so it has no cuts and no bridges.
    tri: Graph = {"X": ["Y", "Z"], "Y": ["X", "Z"], "Z": ["X", "Y"]}
    c, b = find_cut_vertices_and_bridges(tri)
    print(f"triangle -> cuts {sorted(c)}, bridges {b}")


if __name__ == "__main__":
    main()
