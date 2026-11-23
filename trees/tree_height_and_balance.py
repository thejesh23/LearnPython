"""Height, diameter and balance of a binary tree in one post-order pass.

The obvious balance check calls height() on both children at every node and
recomputes the same subtrees again and again: O(n^2) on a long chain. The fix
is to have one recursive function return the height and let the caller check
balance on the way back up, so every node is visited once.

The diameter (the longest path between any two nodes, counted in edges) falls
out of the same pass: the longest path through a node is left height + right
height, and the answer is the best of those over all nodes. Returning -1 as
the height of an empty tree is a common trick to mark "unbalanced" with no
extra flag; here a separate sentinel keeps the two meanings apart.
"""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    left: Node | None = None
    right: Node | None = None


UNBALANCED = -2


def height(node: Node | None) -> int:
    """Height in edges; an empty tree is -1 and a leaf is 0."""
    if node is None:
        return -1
    return 1 + max(height(node.left), height(node.right))


def is_balanced_slow(node: Node | None) -> bool:
    if node is None:
        return True
    return (abs(height(node.left) - height(node.right)) <= 1
            and is_balanced_slow(node.left) and is_balanced_slow(node.right))


def is_balanced(root: Node | None) -> bool:
    def check(node: Node | None) -> int:
        if node is None:
            return -1
        left = check(node.left)
        if left == UNBALANCED:
            return UNBALANCED
        right = check(node.right)
        if right == UNBALANCED or abs(left - right) > 1:
            return UNBALANCED
        return 1 + max(left, right)

    return check(root) != UNBALANCED


def diameter(root: Node | None) -> int:
    best = 0

    def depth(node: Node | None) -> int:
        nonlocal best
        if node is None:
            return -1
        left, right = depth(node.left), depth(node.right)
        best = max(best, left + right + 2)
        return 1 + max(left, right)

    depth(root)
    return best


def random_tree(rng: random.Random, depth: int) -> Node | None:
    if depth == 0 or rng.random() < 0.2:
        return None
    return Node(0, random_tree(rng, depth - 1), random_tree(rng, depth - 1))


def main() -> None:
    #       1
    #      / \
    #     2   3
    #    / \
    #   4   5
    #  /     \
    # 6       7
    tree = Node(1, Node(2, Node(4, Node(6)), Node(5, None, Node(7))), Node(3))
    print(f"height {height(tree)}, diameter {diameter(tree)} (6-4-2-5-7), "
          f"balanced {is_balanced(tree)}")

    perfect = Node(1, Node(2, Node(4), Node(5)), Node(3, Node(6), Node(7)))
    print(f"perfect tree: height {height(perfect)}, balanced {is_balanced(perfect)}")

    chain = Node(1, Node(2, Node(3)))
    print(f"chain of 3:   height {height(chain)}, balanced {is_balanced(chain)}")
    print(f"empty:        height {height(None)}, diameter {diameter(None)}, "
          f"balanced {is_balanced(None)}")

    rng = random.Random(4)
    trees = [random_tree(rng, 7) for _ in range(1500)]
    agree = all(is_balanced(t) == is_balanced_slow(t) for t in trees)
    print(f"\none-pass and naive balance checks agree on 1500 trees: {agree}")
    print(f"balanced among them: {sum(map(is_balanced, trees))}")


if __name__ == "__main__":
    main()
