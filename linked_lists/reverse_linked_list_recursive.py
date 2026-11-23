"""Reversing a singly linked list recursively, and in groups of k.

The iterative three-pointer version lives in data_structures/linked_list.py.
The recursive one reads differently: reverse everything after the head, and
the old second node is now the tail of that reversed list, so hang the head
off it (head.next.next = head) and cut the head's own link. The new head
bubbles up unchanged from the bottom of the recursion.

It costs O(n) stack frames, so on CPython it fails near the recursion limit
(about 1000 nodes), which the demo shows. Reversing in groups of k reuses the
same idea one block at a time: reverse the first k nodes, then recurse on the
rest and attach it to the block's new tail.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    next: Node | None = None


def build(values: list[int]) -> Node | None:
    head = None
    for v in reversed(values):
        head = Node(v, head)
    return head


def to_list(head: Node | None) -> list[int]:
    out: list[int] = []
    while head:
        out.append(head.value)
        head = head.next
    return out


def reverse(head: Node | None) -> Node | None:
    if head is None or head.next is None:
        return head
    new_head = reverse(head.next)
    head.next.next = head
    head.next = None
    return new_head


def reverse_k_group(head: Node | None, k: int) -> Node | None:
    """Reverse each full block of k nodes; a short final block stays as it is."""
    probe, count = head, 0
    while probe and count < k:
        probe, count = probe.next, count + 1
    if count < k:
        return head
    prev, node = reverse_k_group(probe, k), head
    for _ in range(k):
        node.next, prev, node = prev, node, node.next  # type: ignore[union-attr]
    return prev


def main() -> None:
    for values in [[1, 2, 3, 4, 5], [1], []]:
        print(f"reverse {values} -> {to_list(reverse(build(values)))}")

    print()
    for k in [1, 2, 3, 5, 6]:
        result = to_list(reverse_k_group(build([1, 2, 3, 4, 5]), k))
        print(f"k = {k}: {result}")

    ok = all(to_list(reverse(build(list(range(n))))) == list(range(n))[::-1]
             for n in range(50))
    print(f"\nmatches list[::-1] for lengths 0..49: {ok}")

    long_list = build(list(range(sys.getrecursionlimit() + 100)))
    try:
        reverse(long_list)
    except RecursionError:
        print(f"recursion limit hit on {sys.getrecursionlimit() + 100} nodes")


if __name__ == "__main__":
    main()
