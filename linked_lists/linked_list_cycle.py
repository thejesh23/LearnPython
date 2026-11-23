"""Detecting a cycle in a linked list, and finding where it starts.

A visited set answers "is there a cycle?" in O(n) space. Floyd's tortoise and
hare does it in O(1): one pointer moves one step, the other two. Without a
cycle the fast one falls off the end; with one, the fast pointer gains one
step per move inside the loop and must land on the slow one.

Finding the entry point is the clever half. If the tail before the loop has
length mu and the loop has length lam, the meeting point sits a distance k
into the loop where mu + k is a multiple of lam. So a pointer restarted at the
head and one left at the meeting point, both moving one step, meet exactly at
the entry after mu steps. Walking once more around the loop gives lam.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass(eq=False)
class Node:
    value: int
    next: Node | None = field(default=None, repr=False)


def build_with_cycle(n: int, entry: int | None) -> tuple[Node | None, Node | None]:
    """n nodes 0..n-1; the last points back to node `entry` (None: no cycle)."""
    nodes = [Node(i) for i in range(n)]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if nodes and entry is not None:
        nodes[-1].next = nodes[entry]
        return nodes[0], nodes[entry]
    return (nodes[0] if nodes else None), None


def has_cycle_set(head: Node | None) -> bool:
    seen: set[int] = set()
    while head:
        if id(head) in seen:
            return True
        seen.add(id(head))
        head = head.next
    return False


def floyd(head: Node | None) -> tuple[Node, int] | None:
    """Return (entry node, loop length), or None when the list ends."""
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next  # type: ignore[union-attr]
        if slow is fast:
            break
    else:
        return None
    probe = head
    while probe is not slow:
        probe, slow = probe.next, slow.next  # type: ignore[union-attr]
    length, node = 1, probe.next  # type: ignore[union-attr]
    while node is not probe:
        length, node = length + 1, node.next  # type: ignore[union-attr]
    return probe, length  # type: ignore[return-value]


def main() -> None:
    for n, entry in [(6, 2), (6, 0), (6, 5), (1, 0), (6, None), (0, None)]:
        head, _ = build_with_cycle(n, entry)
        result = floyd(head)
        if result:
            node, length = result
            print(f"n={n}, back-link to {entry}: "
                  f"entry {node.value}, loop length {length}")
        else:
            print(f"n={n}, no back-link: no cycle")

    rng = random.Random(2)
    ok = True
    for _ in range(500):
        n = rng.randint(1, 60)
        entry = rng.choice([None, rng.randrange(n)])
        head, expected = build_with_cycle(n, entry)
        result = floyd(head)
        ok &= has_cycle_set(head) == (result is not None)
        if result:
            loop_length = n - entry if entry is not None else 0
            ok &= result[0] is expected and result[1] == loop_length
    print(f"\nentry and length correct, agrees with visited set (500 lists): {ok}")


if __name__ == "__main__":
    main()
