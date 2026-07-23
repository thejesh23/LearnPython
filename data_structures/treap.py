"""Treap: a BST by key and a heap by a random priority, balanced in expectation.

Each node carries a key (kept in BST order) and a priority (kept in max-heap
order). Because the priorities are random, the tree's shape is the shape a
random insertion order would produce — so the height is O(log n) expected, with
no explicit balancing rules to maintain.

Insertion and deletion are expressed through two operations, split and merge,
which is what makes the treap so flexible: split(key) cuts the tree into
"< key" and ">= key" halves, merge glues two ordered trees back. Order
statistics come for free by storing subtree sizes.

Expected O(log n) per operation; the worst case is astronomically unlikely.
"""

import random
from dataclasses import dataclass


@dataclass
class Node:
    key: int
    priority: float
    size: int = 1
    left: "Node | None" = None
    right: "Node | None" = None


def size(node: Node | None) -> int:
    return node.size if node else 0


def update(node: Node) -> Node:
    node.size = 1 + size(node.left) + size(node.right)
    return node


def split(node: Node | None, key: int) -> tuple[Node | None, Node | None]:
    """Into (keys < key, keys >= key)."""
    if node is None:
        return None, None
    if node.key < key:
        left, right = split(node.right, key)
        node.right = left
        return update(node), right
    left, right = split(node.left, key)
    node.left = right
    return left, update(node)


def merge(a: Node | None, b: Node | None) -> Node | None:
    """Merge two treaps where every key in a is < every key in b."""
    if a is None or b is None:
        return a or b
    if a.priority > b.priority:  # a's root wins the heap order
        a.right = merge(a.right, b)
        return update(a)
    b.left = merge(a, b.left)
    return update(b)


class Treap:
    def __init__(self, seed: int = 0) -> None:
        self.root: Node | None = None
        self._rng = random.Random(seed)

    def insert(self, key: int) -> None:
        if self.contains(key):
            return
        left, right = split(self.root, key)
        node = Node(key, self._rng.random())
        self.root = merge(merge(left, node), right)

    def delete(self, key: int) -> None:
        left, right = split(self.root, key)
        _, right_ge = split(right, key + 1)  # peel off exactly `key`
        self.root = merge(left, right_ge)

    def contains(self, key: int) -> bool:
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def kth(self, k: int) -> int:
        """0-indexed k-th smallest, using subtree sizes. O(log n) expected."""
        node = self.root
        while node:
            left_size = size(node.left)
            if k == left_size:
                return node.key
            if k < left_size:
                node = node.left
            else:
                k -= left_size + 1
                node = node.right
        raise IndexError("k out of range")

    def in_order(self) -> list[int]:
        out: list[int] = []

        def walk(node: Node | None) -> None:
            if node:
                walk(node.left)
                out.append(node.key)
                walk(node.right)

        walk(self.root)
        return out

    def height(self) -> int:
        def h(node: Node | None) -> int:
            return 0 if node is None else 1 + max(h(node.left), h(node.right))

        return h(self.root)


def main() -> None:
    treap = Treap(seed=42)
    for key in [5, 3, 8, 1, 4, 7, 9, 2, 6]:
        treap.insert(key)
    print(f"in-order (sorted): {treap.in_order()}")
    print(f"contains 7: {treap.contains(7)}, contains 10: {treap.contains(10)}")
    print(f"3rd smallest (k=2): {treap.kth(2)}")
    print(f"all order statistics: {[treap.kth(k) for k in range(9)]}")

    treap.delete(5)
    treap.delete(1)
    print(f"after deleting 5 and 1: {treap.in_order()}")

    # Random priorities keep the height near log2(n) even for sorted inserts.
    sorted_treap = Treap(seed=1)
    for key in range(1000):
        sorted_treap.insert(key)
    import math

    print(f"1000 sorted inserts -> height {sorted_treap.height()} "
          f"(a plain BST would be 1000; log2 is ~{math.log2(1000):.0f})")
    print(f"still fully sorted: {sorted_treap.in_order() == list(range(1000))}")


if __name__ == "__main__":
    main()
