"""Binary search: halve the range on every comparison. Requires sorted input.

Two details cause most of the bugs ever written in this function:
  - `mid = lo + (hi - lo) // 2` avoids overflow in fixed-width languages.
    Python ints cannot overflow, but the habit is worth keeping.
  - The loop must shrink the range every iteration, or it hangs. With the
    inclusive `hi` used here, `while lo <= hi` plus `mid ± 1` guarantees it.

Complexity: O(log n) time, O(1) space.
"""

from bisect import bisect_left, bisect_right


def binary_search(values: list[int], target: int) -> int:
    lo, hi = 0, len(values) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if values[mid] == target:
            return mid
        if values[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def lower_bound(values: list[int], target: int) -> int:
    """First index whose value is >= target — the insertion point."""
    lo, hi = 0, len(values)
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(values: list[int], target: int) -> int:
    """First index whose value is > target."""
    lo, hi = 0, len(values)
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def main() -> None:
    data = [1, 3, 3, 3, 5, 7, 9]
    print(f"binary_search(7) = {binary_search(data, 7)}")
    print(f"binary_search(4) = {binary_search(data, 4)}")
    print(f"lower_bound(3) = {lower_bound(data, 3)}, upper_bound(3) = {upper_bound(data, 3)}")
    print(f"count of 3 = {upper_bound(data, 3) - lower_bound(data, 3)}")
    # The standard library ships both bounds.
    print(f"bisect_left(3) = {bisect_left(data, 3)}, bisect_right(3) = {bisect_right(data, 3)}")


if __name__ == "__main__":
    main()
