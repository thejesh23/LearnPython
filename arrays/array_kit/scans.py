"""Single-sweep techniques: prefix sums, a monotonic-deque window, Boyer-Moore
voting and interval merging."""

from collections import deque
from collections.abc import Sequence


class PrefixSums:
    """O(n) build, then any ``sum(values[lo:hi])`` in O(1).

    ``prefix[i]`` is the sum of the first i values; the leading zero is what
    makes ``prefix[hi] - prefix[lo]`` work with no special cases.
    """

    def __init__(self, values: Sequence[int]) -> None:
        self.prefix = [0]
        for v in values:
            self.prefix.append(self.prefix[-1] + v)

    def range_sum(self, lo: int, hi: int) -> int:
        """Sum of values[lo:hi], half-open like a slice."""
        return self.prefix[hi] - self.prefix[lo]


def count_subarrays_with_sum(values: Sequence[int], k: int) -> int:
    """How many contiguous subarrays sum to k, via a map of seen prefix sums."""
    seen = {0: 1}
    running = total = 0
    for v in values:
        running += v
        total += seen.get(running - k, 0)
        seen[running] = seen.get(running, 0) + 1
    return total


def window_max(values: Sequence[int], k: int) -> list[int]:
    """Maximum of every length-k window in O(n) with a decreasing deque of indices."""
    if k <= 0:
        return []
    window: deque[int] = deque()
    out: list[int] = []
    for i, value in enumerate(values):
        while window and values[window[-1]] <= value:
            window.pop()  # smaller and older: it can never be a max again
        window.append(i)
        if window[0] <= i - k:
            window.popleft()  # slid out of the window
        if i >= k - 1:
            out.append(values[window[0]])
    return out


def majority(values: Sequence[int]) -> int | None:
    """The element occurring more than n/2 times (Boyer-Moore vote), or None."""
    candidate, count = None, 0
    for v in values:
        if count == 0:
            candidate = v
        count += 1 if v == candidate else -1
    # The vote only nominates; a second pass confirms.
    if candidate is not None and list(values).count(candidate) > len(values) // 2:
        return candidate
    return None


def merge_intervals(intervals: Sequence[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge overlapping or touching closed intervals: sort by start, then sweep."""
    merged: list[tuple[int, int]] = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged
