"""Merging two sorted linked lists by relinking nodes, not copying them.

A dummy head node removes the special case for "which list supplies the
first node": the merge always appends after tail, and the answer is
dummy.next. At each step, take the smaller front node, link it in, and advance
that list. When one list runs out, the other is already sorted, so it is
attached in a single pointer write instead of a loop.

Cost is O(n + m) time and O(1) extra space, since no node is created. Taking
from the left list on ties keeps the merge stable. Merging k lists pairwise in
rounds (1+2, 3+4, ...) gives O(N log k) total work, the same bound as a heap.
"""

from __future__ import annotations

import heapq
import random
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    next: Node | None = None
    tag: str = ""


def build(values: list[int], tag: str = "") -> Node | None:
    head = None
    for v in reversed(values):
        head = Node(v, head, tag)
    return head


def to_list(head: Node | None) -> list[int]:
    out: list[int] = []
    while head:
        out.append(head.value)
        head = head.next
    return out


def merge(a: Node | None, b: Node | None) -> Node | None:
    dummy = tail = Node(0)
    while a and b:
        if a.value <= b.value:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


def merge_k(lists: list[Node | None]) -> Node | None:
    if not lists:
        return None
    while len(lists) > 1:
        paired = [merge(lists[i], lists[i + 1]) for i in range(0, len(lists) - 1, 2)]
        if len(lists) % 2:
            paired.append(lists[-1])
        lists = paired
    return lists[0]


def main() -> None:
    a, b = build([1, 3, 5, 7]), build([2, 3, 6])
    print(f"merge: {to_list(merge(a, b))}")
    print(f"one empty: {to_list(merge(build([]), build([4, 9])))}")
    print(f"both empty: {to_list(merge(None, None))}")

    left, right = build([1, 2, 2], "L"), build([2, 3], "R")
    node, tags = merge(left, right), []
    while node:
        tags.append(f"{node.value}{node.tag}")
        node = node.next
    print(f"stable on ties: {tags}")

    rng = random.Random(3)
    runs = [sorted(rng.choices(range(100), k=rng.randint(0, 8))) for _ in range(7)]
    merged = to_list(merge_k([build(r) for r in runs]))
    print(f"\nmerge_k of {len(runs)} lists: {merged[:12]}...")
    print(f"matches heapq.merge: {merged == list(heapq.merge(*runs))}")

    ok = True
    for _ in range(300):
        x = sorted(rng.choices(range(20), k=rng.randint(0, 10)))
        y = sorted(rng.choices(range(20), k=rng.randint(0, 10)))
        ok &= to_list(merge(build(x), build(y))) == sorted(x + y)
    print(f"matches sorted(x + y) on 300 random pairs: {ok}")


if __name__ == "__main__":
    main()
