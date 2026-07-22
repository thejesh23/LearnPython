"""Adjacency list vs adjacency matrix — the choice that shapes every algorithm.

    adjacency list    O(V + E) space, O(deg(v)) to list neighbours,
                      O(deg(v)) to test an edge. Right for sparse graphs.
    adjacency matrix  O(V^2) space, O(1) edge test, O(V) to list neighbours.
                      Right for dense graphs and for matrix algorithms
                      (Floyd-Warshall, transitive closure).

Most real graphs are sparse (E ~ V, not V^2), which is why the list wins by
default. A dict-of-dicts adds edge weights without changing the shape.
"""


class Graph:
    """Adjacency list, undirected or directed, optionally weighted."""

    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self.adj: dict[str, dict[str, float]] = {}

    def add_node(self, node: str) -> None:
        self.adj.setdefault(node, {})

    def add_edge(self, a: str, b: str, weight: float = 1.0) -> None:
        self.add_node(a)
        self.add_node(b)
        self.adj[a][b] = weight
        if not self.directed:
            self.adj[b][a] = weight

    def neighbours(self, node: str) -> list[str]:
        return list(self.adj.get(node, {}))

    def has_edge(self, a: str, b: str) -> bool:
        return b in self.adj.get(a, {})

    def degree(self, node: str) -> int:
        return len(self.adj.get(node, {}))

    @property
    def nodes(self) -> list[str]:
        return list(self.adj)

    @property
    def edges(self) -> list[tuple[str, str, float]]:
        seen: set[frozenset[str]] = set()
        out: list[tuple[str, str, float]] = []
        for a, links in self.adj.items():
            for b, w in links.items():
                key = frozenset((a, b))
                if not self.directed and key in seen:
                    continue
                seen.add(key)
                out.append((a, b, w))
        return out

    def to_matrix(self) -> tuple[list[str], list[list[float]]]:
        order = sorted(self.adj)
        index = {node: i for i, node in enumerate(order)}
        size = len(order)
        matrix = [[0.0] * size for _ in range(size)]
        for a, links in self.adj.items():
            for b, w in links.items():
                matrix[index[a]][index[b]] = w
        return order, matrix


def main() -> None:
    g = Graph()
    for a, b, w in [("A", "B", 1), ("A", "C", 4), ("B", "C", 2), ("C", "D", 3)]:
        g.add_edge(a, b, w)

    print(f"nodes: {g.nodes}")
    print(f"edges: {g.edges}")
    print(f"neighbours of C: {g.neighbours('C')}")
    print(f"has_edge(A, D): {g.has_edge('A', 'D')}, degree(C): {g.degree('C')}")

    order, matrix = g.to_matrix()
    print(f"matrix over {order}:")
    for name, row in zip(order, matrix):
        print(f"  {name}: {row}")

    directed = Graph(directed=True)
    directed.add_edge("X", "Y")
    print(f"directed: X->Y {directed.has_edge('X', 'Y')}, "
          f"Y->X {directed.has_edge('Y', 'X')}")

    v, e = 10_000, 30_000
    print(f"\n{v} nodes, {e} edges:")
    print(f"  list  ~ V + 2E = {v + 2 * e} entries")
    print(f"  matrix ~ V^2   = {v * v} entries ({v * v // (v + 2 * e)}x more)")


if __name__ == "__main__":
    main()
