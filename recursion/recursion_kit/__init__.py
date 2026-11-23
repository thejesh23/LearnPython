"""recursion_kit: permutations, combinations, subsets, flatten, Hanoi, Ackermann.

    >>> from recursion.recursion_kit import combinations, hanoi
    >>> combinations([1, 2, 3], 2)
    [[1, 2], [1, 3], [2, 3]]
    >>> hanoi(2)
    [('A', 'B'), ('A', 'C'), ('B', 'C')]
"""

from .combinatorics import combinations, permutations, power_set
from .structure import ackermann, depth, flatten, hanoi, recursion_limit

__all__ = [
    "permutations",
    "combinations",
    "power_set",
    "flatten",
    "depth",
    "hanoi",
    "ackermann",
    "recursion_limit",
]
