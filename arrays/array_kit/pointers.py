"""Index-pointer techniques: hash-map two sum, two pointers, read/write
compaction, three-way partition and rotation by reversal.

Every function returns a new list and leaves its input untouched.
"""

from collections.abc import Sequence


def two_sum(values: Sequence[int], target: int) -> tuple[int, int] | None:
    """Indices (i, j), i < j, with values[i] + values[j] == target, or None.

    One pass: ask "has the complement already been seen?" instead of
    pairing every element with every later one. O(n) time and space.
    """
    seen: dict[int, int] = {}  # value -> index
    for j, value in enumerate(values):
        i = seen.get(target - value)
        if i is not None:
            return i, j
        seen.setdefault(value, j)
    return None


def three_sum(values: Sequence[int], target: int = 0) -> list[tuple[int, int, int]]:
    """Every distinct sorted triple summing to target: sort, then two pointers."""
    a = sorted(values)
    out: list[tuple[int, int, int]] = []
    for i in range(len(a) - 2):
        if i and a[i] == a[i - 1]:
            continue  # same anchor value, same triples
        lo, hi = i + 1, len(a) - 1
        while lo < hi:
            total = a[i] + a[lo] + a[hi]
            if total < target:
                lo += 1
            elif total > target:
                hi -= 1
            else:
                out.append((a[i], a[lo], a[hi]))
                lo += 1
                while lo < hi and a[lo] == a[lo - 1]:
                    lo += 1
                hi -= 1
    return out


def move_zeroes(values: Sequence[int]) -> list[int]:
    """Zeroes to the back, non-zero order kept: the read/write pointer pattern."""
    a = list(values)
    write = 0
    for read in range(len(a)):
        if a[read] != 0:
            a[write], a[read] = a[read], a[write]
            write += 1
    return a


def partition3(values: Sequence[int], pivot: int) -> list[int]:
    """Dutch national flag: < pivot, == pivot, > pivot in one pass, O(1) space.

    Regions: [0, low) less, [low, mid) equal, [mid, high] unknown, (high, n)
    greater. A swap from the back does not advance mid: that value is unseen.
    """
    a = list(values)
    low, mid, high = 0, 0, len(a) - 1
    while mid <= high:
        if a[mid] < pivot:
            a[low], a[mid] = a[mid], a[low]
            low += 1
            mid += 1
        elif a[mid] == pivot:
            mid += 1
        else:
            a[mid], a[high] = a[high], a[mid]
            high -= 1
    return a


def rotate(values: Sequence[int], k: int) -> list[int]:
    """Rotate right by k (left if negative) with three in-place reversals."""
    a = list(values)
    n = len(a)
    if n == 0:
        return a
    k %= n

    def reverse(lo: int, hi: int) -> None:
        while lo < hi:
            a[lo], a[hi] = a[hi], a[lo]
            lo, hi = lo + 1, hi - 1

    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)
    return a
