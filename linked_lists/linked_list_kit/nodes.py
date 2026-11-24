"""Singly linked nodes and the helpers every list algorithm needs."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field


@dataclass(eq=False)
class Node:
    value: int
    next: Node | None = field(default=None, repr=False)


def from_values(values: Iterable[int]) -> Node | None:
    """Build a list front to back and return its head (None when empty)."""
    dummy = tail = Node(0)
    for v in values:
        tail.next = Node(v)
        tail = tail.next
    return dummy.next


def iter_nodes(head: Node | None, limit: int = 1_000_000) -> Iterator[Node]:
    """Yield nodes in order; stops with an error rather than loop forever."""
    for _ in range(limit):
        if head is None:
            return
        yield head
        head = head.next
    raise ValueError("list is longer than the limit; is there a cycle?")


def to_values(head: Node | None) -> list[int]:
    return [node.value for node in iter_nodes(head)]


def show(head: Node | None) -> str:
    return " -> ".join(map(str, to_values(head))) or "(empty)"
