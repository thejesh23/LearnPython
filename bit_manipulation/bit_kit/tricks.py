"""Xor puzzles and bitmask enumeration.

Xor is its own inverse (x ^ x == 0, x ^ 0 == x) and order does not matter,
so xor-ing a list cancels every pair. An n-bit integer is a subset of n items,
so counting from 0 to 2**n - 1 walks every subset.
"""

from collections.abc import Sequence
from functools import reduce
from operator import xor
from typing import Any


def single_number(nums: Sequence[int]) -> int:
    """The one value that appears an odd number of times when all others pair up."""
    return reduce(xor, nums, 0)


def two_single_numbers(nums: Sequence[int]) -> tuple[int, int]:
    """The two unpaired values (smaller first) when every other value appears twice.

    Xor of everything is a ^ b; any set bit of it separates a from b, so
    xor-ing just the numbers with that bit set isolates one of them.
    """
    both = reduce(xor, nums, 0)
    if both == 0:
        raise ValueError("no two distinct unpaired values")
    split = both & -both
    a = reduce(xor, (n for n in nums if n & split), 0)
    b = both ^ a
    return (a, b) if a <= b else (b, a)


def missing_number(nums: Sequence[int]) -> int:
    """The one value missing from 0..len(nums): xor the list against the full range."""
    return reduce(xor, nums, 0) ^ reduce(xor, range(len(nums) + 1), 0)


def subsets(items: Sequence[Any]) -> list[list[Any]]:
    """All 2**n subsets; subset number ``mask`` holds items[i] when bit i is set."""
    n = len(items)
    return [[items[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n)]


def submasks(mask: int) -> list[int]:
    """Every submask of mask, largest first, via ``(sub - 1) & mask``."""
    out, sub = [], mask
    while sub:
        out.append(sub)
        sub = (sub - 1) & mask
    out.append(0)
    return out
