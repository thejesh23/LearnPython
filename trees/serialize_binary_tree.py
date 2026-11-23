"""Serializing a binary tree to a string and rebuilding it exactly.

A traversal alone loses the shape: the trees 1 -> left 2 and 1 -> right 2
have the same preorder. Writing a marker for every missing child fixes that.
Preorder with "#" for None is the shortest code to write and to read back: the
reader consumes tokens in the same order the writer produced them, building
the left subtree before the right, recursion mirroring recursion.

Level order with trailing markers trimmed is the format LeetCode and many
tools print, and it is easier for people to read. Both are O(n) in time and
output length. Without markers, a tree can be rebuilt only from two
traversals together, such as preorder plus inorder with unique values.
"""

from __future__ import annotations

import random
from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    left: Node | None = None
    right: Node | None = None


def to_preorder(root: Node | None) -> str:
    tokens: list[str] = []

    def walk(node: Node | None) -> None:
        if node is None:
            tokens.append("#")
            return
        tokens.append(str(node.value))
        walk(node.left)
        walk(node.right)

    walk(root)
    return ",".join(tokens)


def from_preorder(text: str) -> Node | None:
    tokens: Iterator[str] = iter(text.split(","))

    def read() -> Node | None:
        token = next(tokens)
        if token == "#":
            return None
        node = Node(int(token))
        node.left = read()
        node.right = read()
        return node

    return read()


def to_level_order(root: Node | None) -> str:
    tokens: list[str] = []
    queue: deque[Node | None] = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            tokens.append("null")
            continue
        tokens.append(str(node.value))
        queue.extend((node.left, node.right))
    while tokens and tokens[-1] == "null":
        tokens.pop()
    return "[" + ",".join(tokens) + "]"


def from_level_order(text: str) -> Node | None:
    tokens = [t for t in text.strip("[]").split(",") if t]
    if not tokens or tokens[0] == "null":
        return None
    root = Node(int(tokens[0]))
    queue, i = deque([root]), 1
    while queue and i < len(tokens):
        node = queue.popleft()
        for side in ("left", "right"):
            if i < len(tokens) and tokens[i] != "null":
                child = Node(int(tokens[i]))
                setattr(node, side, child)
                queue.append(child)
            i += 1
    return root


def random_tree(rng: random.Random, depth: int) -> Node | None:
    if depth == 0 or rng.random() < 0.3:
        return None
    return Node(rng.randint(-50, 50), random_tree(rng, depth - 1),
                random_tree(rng, depth - 1))


def main() -> None:
    tree = Node(1, Node(2), Node(3, Node(4), Node(5)))
    print(f"preorder:    {to_preorder(tree)}")
    print(f"level order: {to_level_order(tree)}")

    lefty, righty = Node(1, Node(2)), Node(1, None, Node(2))
    print(f"\nsame preorder values, different shapes:")
    print(f"  left child:  {to_preorder(lefty):<12} {to_level_order(lefty)}")
    print(f"  right child: {to_preorder(righty):<12} {to_level_order(righty)}")
    print(f"empty: {to_preorder(None)!r} {to_level_order(None)}")

    rng = random.Random(12)
    trees = [random_tree(rng, 7) for _ in range(1000)]
    pre_ok = all(from_preorder(to_preorder(t)) == t for t in trees)
    level_ok = all(from_level_order(to_level_order(t)) == t for t in trees)
    print(f"\npreorder round trip on 1000 random trees: {pre_ok}")
    print(f"level-order round trip on 1000 random trees: {level_ok}")


if __name__ == "__main__":
    main()
