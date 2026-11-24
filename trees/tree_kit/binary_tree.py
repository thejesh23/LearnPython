"""Binary tree nodes, level-order (de)serialisation, traversals and shape.

Traversals use explicit stacks and queues, so deep trees never hit the
recursion limit.
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
    """[1, 2, 3, None, 4] -> the tree LeetCode prints that way."""
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


def to_level_order(root: Node | None) -> list[int | None]:
    out: list[int | None] = []
    queue: deque[Node | None] = deque([root])
    while queue:
        node = queue.popleft()
        out.append(node.value if node else None)
        if node:
            queue.extend((node.left, node.right))
    while out and out[-1] is None:
        out.pop()
    return out


def preorder(root: Node | None) -> Iterator[int]:
    stack = [root] if root else []
    while stack:
        node = stack.pop()
        yield node.value
        stack.extend(child for child in (node.right, node.left) if child)


def inorder(root: Node | None) -> Iterator[int]:
    stack: list[Node] = []
    node = root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        yield node.value
        node = node.right


def postorder(root: Node | None) -> Iterator[int]:
    out: list[int] = []
    stack = [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.value)
        stack.extend(child for child in (node.left, node.right) if child)
    yield from reversed(out)


def levels(root: Node | None) -> list[list[int]]:
    rows: list[list[int]] = []
    queue = deque([root] if root else [])
    while queue:
        rows.append([])
        for _ in range(len(queue)):
            node = queue.popleft()
            rows[-1].append(node.value)
            queue.extend(child for child in (node.left, node.right) if child)
    return rows


def shape(root: Node | None) -> tuple[int, int, bool]:
    """(height in edges, diameter in edges, balanced?) in one post-order pass."""
    info: dict[int, tuple[int, bool]] = {}  # id(node) -> (height, balanced)
    diameter = 0
    stack: list[tuple[Node, bool]] = [(root, False)] if root else []
    while stack:
        node, children_done = stack.pop()
        if not children_done:
            stack.append((node, True))
            stack.extend((c, False) for c in (node.left, node.right) if c)
            continue
        lh, lb = info.get(id(node.left), (-1, True)) if node.left else (-1, True)
        rh, rb = info.get(id(node.right), (-1, True)) if node.right else (-1, True)
        diameter = max(diameter, lh + rh + 2)
        info[id(node)] = (1 + max(lh, rh), lb and rb and abs(lh - rh) <= 1)
    if root is None:
        return -1, 0, True
    height, balanced = info[id(root)]
    return height, diameter, balanced
