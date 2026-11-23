"""Root-to-leaf paths, target path sums, and the maximum path sum.

Collecting every root-to-leaf path is a depth-first walk that carries the path
so far, appending on the way down and popping on the way back (backtracking),
so one list is shared instead of copying it at every node.

"Is there a root-to-leaf path summing to target?" subtracts each value from
the target on the way down and checks for zero at a leaf. Counting paths that
may start and end anywhere going downward uses prefix sums: if the running sum
at a node minus target appeared earlier on the current path, the stretch
between them sums to target. That turns O(n^2) into O(n).

The maximum path sum may bend through a node and skip negative branches, so
each node reports upward only its best single downward arm, clamped at zero.
"""

from __future__ import annotations

import random
from collections import Counter
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    left: Node | None = None
    right: Node | None = None


def all_paths(root: Node | None) -> list[list[int]]:
    paths: list[list[int]] = []
    path: list[int] = []

    def walk(node: Node | None) -> None:
        if node is None:
            return
        path.append(node.value)
        if node.left is None and node.right is None:
            paths.append(path.copy())
        walk(node.left)
        walk(node.right)
        path.pop()

    walk(root)
    return paths


def has_path_sum(node: Node | None, target: int) -> bool:
    if node is None:
        return False
    rest = target - node.value
    if node.left is None and node.right is None:
        return rest == 0
    return has_path_sum(node.left, rest) or has_path_sum(node.right, rest)


def count_downward_paths(root: Node | None, target: int) -> int:
    seen: Counter[int] = Counter({0: 1})

    def walk(node: Node | None, running: int) -> int:
        if node is None:
            return 0
        running += node.value
        found = seen[running - target]
        seen[running] += 1
        found += walk(node.left, running) + walk(node.right, running)
        seen[running] -= 1
        return found

    return walk(root, 0)


def count_downward_brute(root: Node | None, target: int) -> int:
    def from_here(node: Node | None, rest: int) -> int:
        if node is None:
            return 0
        rest -= node.value
        return (rest == 0) + from_here(node.left, rest) + from_here(node.right, rest)

    if root is None:
        return 0
    return (from_here(root, target) + count_downward_brute(root.left, target)
            + count_downward_brute(root.right, target))


def max_path_sum(root: Node) -> int:
    best = root.value

    def arm(node: Node | None) -> int:
        nonlocal best
        if node is None:
            return 0
        left, right = max(arm(node.left), 0), max(arm(node.right), 0)
        best = max(best, node.value + left + right)
        return node.value + max(left, right)

    arm(root)
    return best


def random_tree(rng: random.Random, depth: int) -> Node | None:
    if depth == 0 or rng.random() < 0.25:
        return None
    return Node(rng.randint(-5, 5), random_tree(rng, depth - 1),
                random_tree(rng, depth - 1))


def main() -> None:
    #          5
    #        /   \
    #       4     8
    #      /     / \
    #     11   13   4
    #    /  \        \
    #   7    2        1
    tree = Node(5, Node(4, Node(11, Node(7), Node(2))),
                Node(8, Node(13), Node(4, None, Node(1))))
    for path in all_paths(tree):
        print(f"  {' -> '.join(map(str, path))}  (sum {sum(path)})")

    print(f"\nroot-to-leaf sum 22: {has_path_sum(tree, 22)}")
    print(f"root-to-leaf sum 23: {has_path_sum(tree, 23)}")
    print(f"downward paths summing to 13: {count_downward_paths(tree, 13)}")

    bendy = Node(-10, Node(9), Node(20, Node(15), Node(7)))
    print(f"\nmax path sum, bending through 20: {max_path_sum(bendy)} (15-20-7)")
    print(f"max path sum, all negative: {max_path_sum(Node(-3, Node(-1)))}")

    rng = random.Random(8)
    ok = True
    for _ in range(800):
        t = random_tree(rng, 6)
        k = rng.randint(-6, 6)
        ok &= count_downward_paths(t, k) == count_downward_brute(t, k)
    print(f"\nprefix-sum count matches brute force on 800 trees: {ok}")


if __name__ == "__main__":
    main()
