"""Recursion that follows the shape of a problem: nested data, Tower of Hanoi,
Ackermann — and how to live with CPython's recursion limit."""

import sys
from collections.abc import Iterator
from contextlib import contextmanager
from functools import cache
from typing import Any


def flatten(nested: list[Any]) -> list[Any]:
    """Leaves of an arbitrarily nested list, left to right."""
    out: list[Any] = []
    for item in nested:
        if isinstance(item, list):
            out.extend(flatten(item))  # the data's shape is the recursion's shape
        else:
            out.append(item)
    return out


def depth(nested: Any) -> int:
    """Nesting depth: 0 for a non-list, 1 for a flat list, and so on."""
    if not isinstance(nested, list):
        return 0
    return 1 + max((depth(item) for item in nested), default=0)


def hanoi(n: int, source: str = "A", target: str = "C", spare: str = "B") -> list[tuple[str, str]]:
    """The 2**n - 1 moves for n discs: park n - 1 on spare, move one, bring n - 1 back."""
    if n == 0:
        return []
    return hanoi(n - 1, source, spare, target) + [(source, target)] + hanoi(n - 1, spare, target, source)


@cache
def ackermann(m: int, n: int) -> int:
    """A(m, n): total and computable, yet not expressible with bounded loops.

    Even A(4, 1) recurses tens of thousands of levels deep; keep m <= 3.
    """
    if m == 0:
        return n + 1
    if n == 0:
        return ackermann(m - 1, 1)
    return ackermann(m - 1, ackermann(m, n - 1))


@contextmanager
def recursion_limit(limit: int) -> Iterator[None]:
    """Temporarily raise the interpreter's recursion limit, restoring it on exit."""
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, limit))
    try:
        yield
    finally:
        sys.setrecursionlimit(old)
