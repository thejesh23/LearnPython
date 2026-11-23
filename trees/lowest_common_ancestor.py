"""Lowest common ancestor of two nodes, three ways.

In a binary search tree the values say which way to go: if both targets are
smaller than the current node, the answer is on the left; if both are larger,
on the right; otherwise the paths split here, so this node is the LCA. That is
O(height) with no extra space.

In a plain binary tree there is no ordering, so search both subtrees. A node
whose left and right searches each found one target is the LCA; otherwise pass
up whichever side found something. O(n), visiting each node once.

With parent pointers it becomes the "intersection of two linked lists"
problem: collect one node's ancestors in a set, then climb from the other
until you hit one. For many queries on a fixed tree, binary lifting
(graphs/lca_binary_lifting.py) answers each in O(log n).
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass(eq=False)
class Node:
    value: int
    left: Node | None = None
    right: Node | None = None
    parent: Node | None = field(default=None, repr=False)


def insert(root: Node | None, value: int) -> Node:
    if root is None:
        return Node(value)
    node = root
    while True:
        side = "left" if value < node.value else "right"
        child = getattr(node, side)
        if child is None:
            setattr(node, side, Node(value, parent=node))
            return root
        node = child


def find(root: Node | None, value: int) -> Node:
    while root and root.value != value:
        root = root.left if value < root.value else root.right
    if root is None:
        raise KeyError(value)
    return root


def label(node: Node | None) -> str:
    return "-" if node is None else str(node.value)


def lca_bst(root: Node | None, a: int, b: int) -> Node | None:
    node = root
    while node:
        if a < node.value and b < node.value:
            node = node.left
        elif a > node.value and b > node.value:
            node = node.right
        else:
            return node
    return None


def lca_binary_tree(node: Node | None, p: Node, q: Node) -> Node | None:
    if node is None or node is p or node is q:
        return node
    left = lca_binary_tree(node.left, p, q)
    right = lca_binary_tree(node.right, p, q)
    if left and right:
        return node
    return left or right


def lca_parents(p: Node, q: Node) -> Node | None:
    ancestors: set[int] = set()
    node: Node | None = p
    while node:
        ancestors.add(id(node))
        node = node.parent
    node = q
    while node and id(node) not in ancestors:
        node = node.parent
    return node


def main() -> None:
    root = None
    for v in [20, 8, 22, 4, 12, 10, 14, 25]:
        root = insert(root, v)
    #        20
    #       /  \
    #      8    22
    #     / \     \
    #    4  12     25
    #      /  \
    #     10  14
    for a, b in [(10, 14), (4, 14), (10, 22), (12, 14), (25, 22)]:
        p, q = find(root, a), find(root, b)
        print(f"lca({a:>2}, {b:>2}): bst {label(lca_bst(root, a, b)):>2}, "
              f"tree {label(lca_binary_tree(root, p, q)):>2}, "
              f"parents {label(lca_parents(p, q)):>2}")

    rng = random.Random(6)
    ok = True
    for _ in range(200):
        values = rng.sample(range(1000), rng.randint(2, 60))
        root = None
        for v in values:
            root = insert(root, v)
        for _ in range(10):
            a, b = rng.sample(values, 2)
            p, q = find(root, a), find(root, b)
            expected = lca_bst(root, a, b)
            ok &= expected is lca_binary_tree(root, p, q) is lca_parents(p, q)
    print(f"\nall three agree on 2000 random queries: {ok}")


if __name__ == "__main__":
    main()
