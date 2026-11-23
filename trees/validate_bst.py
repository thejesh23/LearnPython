r"""Is this binary tree a valid binary search tree?

The tempting check, "each node is greater than its left child and less than
its right child", is wrong: it only looks one level down. In the tree

        5
       / \
      3   8
         /
        4

every parent-child pair is fine, yet 4 sits in 5's right subtree. The real
rule is that every node lies inside an interval inherited from all of its
ancestors. Going left tightens the upper bound, going right tightens the lower
one.

The equivalent check: an inorder traversal of a BST is strictly increasing, so
walk inorder and compare each value with the previous one. Both are O(n).
"""

from __future__ import annotations

import random
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    left: Node | None = None
    right: Node | None = None


def is_bst_bounds(node: Node | None, low: float = float("-inf"),
                  high: float = float("inf")) -> bool:
    if node is None:
        return True
    if not low < node.value < high:
        return False
    return (is_bst_bounds(node.left, low, node.value)
            and is_bst_bounds(node.right, node.value, high))


def _inorder(node: Node | None) -> Iterator[int]:
    if node:
        yield from _inorder(node.left)
        yield node.value
        yield from _inorder(node.right)


def is_bst_inorder(root: Node | None) -> bool:
    values = list(_inorder(root))
    return all(a < b for a, b in zip(values, values[1:]))


def is_bst_local_only(node: Node | None) -> bool:
    """The wrong version: checks only parent-child pairs."""
    if node is None:
        return True
    if node.left and node.left.value >= node.value:
        return False
    if node.right and node.right.value <= node.value:
        return False
    return is_bst_local_only(node.left) and is_bst_local_only(node.right)


def random_tree(rng: random.Random, depth: int) -> Node | None:
    if depth == 0 or rng.random() < 0.25:
        return None
    return Node(rng.randint(0, 20), random_tree(rng, depth - 1),
                random_tree(rng, depth - 1))


def insert(node: Node | None, value: int) -> Node:
    if node is None:
        return Node(value)
    if value < node.value:
        node.left = insert(node.left, value)
    elif value > node.value:
        node.right = insert(node.right, value)
    return node


def main() -> None:
    trap = Node(5, Node(3), Node(8, Node(4)))
    print("the trap tree (4 inside 5's right subtree):")
    print(f"  local check: {is_bst_local_only(trap)}")
    print(f"  bounds:      {is_bst_bounds(trap)}")
    print(f"  inorder:     {is_bst_inorder(trap)}  {list(_inorder(trap))}")

    good = None
    for v in [50, 30, 70, 20, 40, 60, 80]:
        good = insert(good, v)
    print(f"\nbuilt by insertion: {is_bst_bounds(good)}")
    print(f"duplicate value:    {is_bst_bounds(Node(2, Node(2)))}")
    print(f"empty tree:         {is_bst_bounds(None)}")

    rng = random.Random(9)
    trees = [random_tree(rng, 5) for _ in range(2000)]
    agree = all(is_bst_bounds(t) == is_bst_inorder(t) for t in trees)
    fooled = sum(is_bst_local_only(t) and not is_bst_bounds(t) for t in trees)
    print(f"\nbounds and inorder agree on 2000 random trees: {agree}")
    print(f"trees the local check wrongly accepts: {fooled}")


if __name__ == "__main__":
    main()
