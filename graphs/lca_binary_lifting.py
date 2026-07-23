"""Lowest common ancestor via binary lifting: O(log n) per query on a tree.

The lowest common ancestor (LCA) of two nodes is their deepest shared ancestor.
Naively you would walk both nodes up until they meet, which is O(n) per query.
Binary lifting precomputes, for every node, its 2^k-th ancestor for all k up to
log n, stored in an "up" table where up[k][v] is the node 2^k steps above v.
Building it is a simple doubling recurrence: up[k][v] = up[k-1][up[k-1][v]].

A query first lifts the deeper node up to the shallower one's depth by adding
powers of two matching the binary form of the depth gap. If the two are now the
same node, that node is the answer. Otherwise both jump up together by the
largest powers that keep them apart; when no such jump remains they sit on the
LCA's two children, so their common parent is the LCA.

The same tables give distances for free: the number of tree edges between u and
v is depth[u] + depth[v] - 2 * depth[lca(u, v)]. Preprocessing is O(n log n)
time and space; each query and each distance is O(log n).
"""


class LCA:
    def __init__(self, n: int, parent: list[int], root: int = 0) -> None:
        self.n = n
        self.log = max(1, (n - 1).bit_length())
        self.depth = [0] * n
        # up[k][v] = ancestor 2^k above v; -1 means "past the root".
        self.up = [[-1] * n for _ in range(self.log)]

        children: list[list[int]] = [[] for _ in range(n)]
        for v in range(n):
            if v != root:
                children[parent[v]].append(v)

        # Iterative BFS fills depth and the base (k=0) ancestor row.
        self.up[0][root] = -1
        order = [root]
        for v in order:
            for c in children[v]:
                self.depth[c] = self.depth[v] + 1
                self.up[0][c] = v
                order.append(c)

        for k in range(1, self.log):
            for v in range(n):
                mid = self.up[k - 1][v]
                self.up[k][v] = self.up[k - 1][mid] if mid != -1 else -1

    def kth_ancestor(self, v: int, k: int) -> int:
        """The ancestor k levels above v, or -1 if it runs past the root."""
        for i in range(self.log):
            if v == -1:
                break
            if k & (1 << i):
                v = self.up[i][v]
        return v

    def query(self, u: int, v: int) -> int:
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        u = self.kth_ancestor(u, self.depth[u] - self.depth[v])  # equalise depth
        if u == v:
            return u
        for k in range(self.log - 1, -1, -1):
            if self.up[k][u] != self.up[k][v]:
                u, v = self.up[k][u], self.up[k][v]
        return self.up[0][u]

    def distance(self, u: int, v: int) -> int:
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.query(u, v)]


def main() -> None:
    #            0
    #          / | \
    #         1  2  3
    #        / \     \
    #       4   5     6
    #          / \
    #         7   8
    parent = [-1, 0, 0, 0, 1, 1, 3, 5, 5]
    tree = LCA(9, parent, root=0)

    print(f"lca(7, 8) = {tree.query(7, 8)} (expect 5)")
    print(f"lca(4, 8) = {tree.query(4, 8)} (expect 1)")
    print(f"lca(7, 6) = {tree.query(7, 6)} (expect 0)")
    print(f"lca(2, 2) = {tree.query(2, 2)} (expect 2)")
    print(f"lca(1, 4) = {tree.query(1, 4)} (expect 1, ancestor case)")

    print(f"dist(7, 8) = {tree.distance(7, 8)} (expect 2)")
    print(f"dist(4, 6) = {tree.distance(4, 6)} (expect 4)")
    print(f"dist(0, 7) = {tree.distance(0, 7)} (expect 3)")

    # Cross-check every pair against a brute-force ancestor-walk LCA.
    def brute_lca(u: int, v: int) -> int:
        anc_u = set()
        x = u
        while x != -1:
            anc_u.add(x)
            x = parent[x]
        while v not in anc_u:
            v = parent[v]
        return v

    for u in range(9):
        for v in range(9):
            assert tree.query(u, v) == brute_lca(u, v), (u, v)
    print("brute-force LCA check passed for all pairs")

    print(f"kth_ancestor(7, 2) = {tree.kth_ancestor(7, 2)} (expect 1)")
    print(f"kth_ancestor(4, 5) = {tree.kth_ancestor(4, 5)} (past root -> -1)")


if __name__ == "__main__":
    main()
