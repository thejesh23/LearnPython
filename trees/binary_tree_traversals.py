"""The four binary tree traversals, recursively and with explicit stacks.

Depth-first orders differ only in when the node itself is visited: before its
children (preorder), between them (inorder), or after them (postorder).
Breadth-first (level order) visits the tree row by row using a queue.

Recursion is the clearest way to write the depth-first orders, but it uses the
call stack, and a degenerate tree of 10,000 nodes overflows CPython's. Each
order has an iterative form with an explicit stack. Preorder is the easy one;
inorder walks left as far as possible before visiting; postorder is a reversed
"node, right, left" preorder. All of them are O(n) time and O(height) space.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    left: Node | None = None
    right: Node | None = None


def from_level_order(values: list[int | None]) -> Node | None:
    if not values or values[0] is None:
        return None
    root = Node(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        for side in ("left", "right"):
            if i < len(values) and values[i] is not None:
                child = Node(values[i])  # type: ignore[arg-type]
                setattr(node, side, child)
                queue.append(child)
            i += 1
    return root


def preorder(node: Node | None) -> Iterator[int]:
    if node:
        yield node.value
        yield from preorder(node.left)
        yield from preorder(node.right)


def inorder(node: Node | None) -> Iterator[int]:
    if node:
        yield from inorder(node.left)
        yield node.value
        yield from inorder(node.right)


def postorder(node: Node | None) -> Iterator[int]:
    if node:
        yield from postorder(node.left)
        yield from postorder(node.right)
        yield node.value


def preorder_iterative(root: Node | None) -> list[int]:
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.value)
        if node.right:
            stack.append(node.right)  # pushed first so left is popped first
        if node.left:
            stack.append(node.left)
    return out


def inorder_iterative(root: Node | None) -> list[int]:
    out: list[int] = []
    stack: list[Node] = []
    node = root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.value)
        node = node.right
    return out


def postorder_iterative(root: Node | None) -> list[int]:
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.value)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return out[::-1]


def level_order(root: Node | None) -> list[list[int]]:
    levels: list[list[int]] = []
    queue = deque([root] if root else [])
    while queue:
        levels.append([])
        for _ in range(len(queue)):
            node = queue.popleft()
            levels[-1].append(node.value)
            queue.extend(child for child in (node.left, node.right) if child)
    return levels


def main() -> None:
    #        1
    #      /   \
    #     2     3
    #    / \     \
    #   4   5     6
    #      /
    #     7
    root = from_level_order([1, 2, 3, 4, 5, None, 6, None, None, 7])
    orders = [("preorder", preorder, preorder_iterative),
              ("inorder", inorder, inorder_iterative),
              ("postorder", postorder, postorder_iterative)]
    for name, recursive, iterative in orders:
        print(f"{name + ':':<12} {list(recursive(root))}  iterative {iterative(root)}")
    print(f"level order: {level_order(root)}")
    print(f"empty tree:  {list(preorder(None))} {level_order(None)}")

    chain = None
    for v in range(10_000):
        chain = Node(v, left=chain)
    try:
        list(inorder(chain))
    except RecursionError:
        print("\nrecursive inorder on a 10,000-deep chain: RecursionError")
    count = len(inorder_iterative(chain))
    print(f"iterative inorder on the same chain: {count} values")


if __name__ == "__main__":
    main()
