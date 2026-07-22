"""Prefix sums: O(n) preprocessing turns any range-sum query into O(1).

prefix[i] holds the sum of the first i elements, so
    sum(a[lo:hi]) == prefix[hi] - prefix[lo]
The leading zero is what makes that formula work without special cases.

The same idea powers subarray-sum-equals-k (a hash map of seen prefix sums)
and the difference array, which applies range *updates* in O(1) each.
"""

from itertools import accumulate


def build_prefix(values: list[int]) -> list[int]:
    prefix = [0]
    for v in values:
        prefix.append(prefix[-1] + v)
    return prefix


def range_sum(prefix: list[int], lo: int, hi: int) -> int:
    """Sum of values[lo:hi] — half-open, like a slice."""
    return prefix[hi] - prefix[lo]


def subarray_sum_count(values: list[int], k: int) -> int:
    """How many subarrays sum to k. O(n) with a map of prefix-sum frequencies."""
    seen = {0: 1}
    running = total = 0
    for v in values:
        running += v
        total += seen.get(running - k, 0)
        seen[running] = seen.get(running, 0) + 1
    return total


def difference_array(length: int, updates: list[tuple[int, int, int]]) -> list[int]:
    """Apply range increments in O(1) each, then integrate once."""
    diff = [0] * (length + 1)
    for lo, hi, delta in updates:  # add delta to [lo, hi)
        diff[lo] += delta
        diff[hi] -= delta
    return list(accumulate(diff[:-1]))


def main() -> None:
    data = [3, 1, 4, 1, 5, 9, 2]
    prefix = build_prefix(data)
    print(f"prefix = {prefix}")
    print(f"sum(data[2:5]) = {range_sum(prefix, 2, 5)} (check {sum(data[2:5])})")
    print(f"accumulate    = {list(accumulate(data))}")
    print(f"subarrays summing to 5: {subarray_sum_count([1, 2, 3, 0, 5], 5)}")
    print(f"difference array: {difference_array(6, [(0, 3, 2), (2, 6, 5)])}")


if __name__ == "__main__":
    main()
