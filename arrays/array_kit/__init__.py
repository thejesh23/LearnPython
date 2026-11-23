"""array_kit: the core array patterns — two pointers, prefix sums, windows.

    >>> from arrays.array_kit import two_sum, window_max
    >>> two_sum([2, 7, 11, 15], 9)
    (0, 1)
    >>> window_max([1, 3, -1, -3, 5, 3, 6, 7], 3)
    [3, 3, 5, 5, 6, 7]
"""

from .pointers import move_zeroes, partition3, rotate, three_sum, two_sum
from .scans import PrefixSums, count_subarrays_with_sum, majority, merge_intervals, window_max

__all__ = [
    "two_sum",
    "three_sum",
    "move_zeroes",
    "partition3",
    "rotate",
    "PrefixSums",
    "count_subarrays_with_sum",
    "window_max",
    "majority",
    "merge_intervals",
]
