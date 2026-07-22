"""Disjoint set (union-find): near-O(1) "are these two in the same group?".

Each set is a tree; the root identifies the set. Two optimisations make it
fast, and both are needed:

  path compression  find() re-parents every node it walks straight to the root
  union by rank     the shorter tree is attached under the taller one

Together they give an amortised cost of O(α(n)) — the inverse Ackermann
function, which is below 5 for any n you will ever have.

Uses: Kruskal's MST, connected components, cycle detection in an undirected
graph, and any "merge these groups" problem.
"""


class DisjointSet:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size
        self.count = size  # number of disjoint sets

    def find(self, x: int) -> int:
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:  # path compression, iterative
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False  # already together
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.count -= 1
        return True

    def connected(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)

    def groups(self) -> dict[int, list[int]]:
        out: dict[int, list[int]] = {}
        for i in range(len(self.parent)):
            out.setdefault(self.find(i), []).append(i)
        return out


def has_cycle(n: int, edges: list[tuple[int, int]]) -> bool:
    """An undirected edge joining two already-connected nodes closes a cycle."""
    dsu = DisjointSet(n)
    return any(not dsu.union(a, b) for a, b in edges)


def main() -> None:
    dsu = DisjointSet(10)
    for a, b in [(0, 1), (1, 2), (3, 4), (5, 6), (6, 7), (7, 5)]:
        dsu.union(a, b)

    print(f"connected(0, 2): {dsu.connected(0, 2)}")
    print(f"connected(0, 3): {dsu.connected(0, 3)}")
    print(f"disjoint sets: {dsu.count}")
    print(f"groups: {dsu.groups()}")

    print(f"cycle in a triangle: {has_cycle(3, [(0, 1), (1, 2), (2, 0)])}")
    print(f"cycle in a path:     {has_cycle(3, [(0, 1), (1, 2)])}")

    # Path compression flattens the tree as a side effect of querying.
    chain = DisjointSet(6)
    for i in range(5):
        chain.parent[i + 1] = i  # deliberately deep chain
    print(f"before find: parents {chain.parent}")
    chain.find(5)
    print(f"after find(5): parents {chain.parent}")


if __name__ == "__main__":
    main()
