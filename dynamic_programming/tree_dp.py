"""Dynamic programming on a rooted tree: three classic subtree recurrences.

A tree has no cycles, so every problem over connected subgraphs decomposes along
children: the answer for a node is a small formula in the answers for its
subtrees. We root the tree once and compute bottom-up.

Three canonical DPs share that one traversal here. Subtree sizes:
size[v] = 1 + sum of size[child]. Maximum weight independent set: no two chosen
nodes may be adjacent, so take[v] weighs v plus every child's skip value, while
skip[v] sums each child's better of take/skip; the answer is max at the root.
Tree diameter: the longest path between any two nodes, found in linear time by
two depth passes — from any node reach a farthest node u, then from u the
farthest node's distance is the diameter (a standard tree fact).

All three run in O(n) over the n nodes. The recursion is written iteratively
where recursion depth could otherwise be a concern, but plain DFS suffices at
these sizes.

Complexity: O(n) time and O(n) space for each pass.
"""

Graph = dict[int, list[int]]


def build_tree(edges: list[tuple[int, int]], n: int) -> Graph:
    g: Graph = {v: [] for v in range(n)}
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    return g


def subtree_sizes(g: Graph, root: int) -> dict[int, int]:
    size: dict[int, int] = {}

    def dfs(v: int, parent: int) -> int:
        s = 1
        for w in g[v]:
            if w != parent:
                s += dfs(w, v)
        size[v] = s
        return s

    dfs(root, -1)
    return size


def max_independent_set(g: Graph, root: int,
                        weight: dict[int, int]) -> int:
    def dfs(v: int, parent: int) -> tuple[int, int]:
        take, skip = weight[v], 0
        for w in g[v]:
            if w != parent:
                ct, cs = dfs(w, v)
                take += cs           # if v is taken, children must be skipped
                skip += max(ct, cs)  # if v is skipped, take each child's best
        return take, skip

    return max(dfs(root, -1))


def _farthest(g: Graph, start: int) -> tuple[int, int]:
    """Return (node, distance) of the farthest node from start via BFS depth."""
    dist = {start: 0}
    stack = [start]
    best_node, best_dist = start, 0
    while stack:
        v = stack.pop()
        for w in g[v]:
            if w not in dist:
                dist[w] = dist[v] + 1
                if dist[w] > best_dist:
                    best_node, best_dist = w, dist[w]
                stack.append(w)
    return best_node, best_dist


def tree_diameter(g: Graph) -> int:
    """Longest path (in edges) via the two-pass method."""
    if not g:
        return 0
    any_node = next(iter(g))
    u, _ = _farthest(g, any_node)
    _, diameter = _farthest(g, u)
    return diameter


def brute_diameter(g: Graph) -> int:
    best = 0
    for s in g:
        _, d = _farthest(g, s)
        best = max(best, d)
    return best


def main() -> None:
    #        0
    #      / | \
    #     1  2  3
    #    /|      \
    #   4 5        6
    edges = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (3, 6)]
    n = 7
    g = build_tree(edges, n)

    print(f"subtree sizes (root 0): {subtree_sizes(g, 0)}")

    weight = {v: 1 for v in range(n)}
    print(f"max independent set, unit weights: {max_independent_set(g, 0, weight)}")
    weight2 = {0: 10, 1: 1, 2: 1, 3: 1, 4: 5, 5: 5, 6: 5}
    print(f"max independent set, weighted:     {max_independent_set(g, 0, weight2)}")

    print(f"diameter (edges): {tree_diameter(g)}")
    assert tree_diameter(g) == brute_diameter(g)

    print("\nedge cases:")
    single = build_tree([], 1)
    print("  single node: sizes", subtree_sizes(single, 0),
          "diameter", tree_diameter(single))
    path = build_tree([(0, 1), (1, 2), (2, 3), (3, 4)], 5)
    print("  path of 5: diameter", tree_diameter(path),
          "MIS(unit)", max_independent_set(path, 0, {v: 1 for v in range(5)}))
    assert tree_diameter(path) == 4


if __name__ == "__main__":
    main()
