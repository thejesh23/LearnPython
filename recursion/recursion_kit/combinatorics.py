"""Generating permutations, combinations and subsets by recursion.

Each generator keeps one partial answer, makes a choice, recurses, then undoes
the choice. Results are copied when recorded because the partial answer keeps
changing afterwards.
"""

from collections.abc import Sequence
from typing import Any


def permutations(items: Sequence[Any], unique: bool = False) -> list[list[Any]]:
    """Every ordering of items by the swap method: fix slot k, recurse on k + 1.

    With ``unique=True`` a value that has already sat in slot k is skipped, so
    repeated items do not produce repeated orderings.
    """
    a = list(items)
    out: list[list[Any]] = []

    def fill(k: int) -> None:
        if k == len(a):
            out.append(list(a))
            return
        tried: list[Any] = []  # a list, so unhashable items work too
        for i in range(k, len(a)):
            if unique and a[i] in tried:
                continue
            tried.append(a[i])
            a[k], a[i] = a[i], a[k]
            fill(k + 1)
            a[k], a[i] = a[i], a[k]  # undo, restoring the caller's order

    fill(0)
    return out


def combinations(items: Sequence[Any], k: int) -> list[list[Any]]:
    """Every k-element selection, in input order; stops when too few items remain."""
    out: list[list[Any]] = []
    chosen: list[Any] = []

    def pick(start: int) -> None:
        if len(chosen) == k:
            out.append(list(chosen))
            return
        for i in range(start, len(items) - (k - len(chosen)) + 1):
            chosen.append(items[i])
            pick(i + 1)
            chosen.pop()

    if 0 <= k <= len(items):
        pick(0)
    return out


def power_set(items: Sequence[Any]) -> list[list[Any]]:
    """All 2**n subsets: one exclude/include decision per item."""
    out: list[list[Any]] = []
    chosen: list[Any] = []

    def decide(i: int) -> None:
        if i == len(items):
            out.append(list(chosen))
            return
        decide(i + 1)  # leave items[i] out
        chosen.append(items[i])
        decide(i + 1)  # put items[i] in
        chosen.pop()

    decide(0)
    return out
