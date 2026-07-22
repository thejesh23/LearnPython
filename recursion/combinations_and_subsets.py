"""Combinations and subsets: choosing without regard to order.

Every subset problem reduces to one binary decision per element: include it or
do not. Recursing on that decision at index i, with the rest of the list left
to decide, enumerates the power set in 2^n leaves. Fixing the number of chosen
elements to k gives combinations instead, and the same recursion works if you
carry the remaining quota and stop when it hits zero.

Two prunings make the k-subset version efficient: stop once the quota is zero,
and stop once there are fewer elements left than the quota still needs.

Because a subset of an n-element list is exactly an n-bit pattern, the whole
power set can also be read off the integers 0 .. 2^n - 1, testing bit i to
decide whether element i is in. That version is iterative and often the fastest
in practice. There are C(n, k) k-subsets and 2^n subsets overall, so both are
output-bound.
"""

from itertools import combinations as it_combinations


def combinations(items: list[int], k: int) -> list[list[int]]:
    result: list[list[int]] = []
    chosen: list[int] = []

    def recurse(start: int) -> None:
        if len(chosen) == k:
            result.append(list(chosen))
            return
        need = k - len(chosen)
        # Stop early when too few elements remain to ever reach size k.
        for i in range(start, len(items) - need + 1):
            chosen.append(items[i])
            recurse(i + 1)
            chosen.pop()

    if 0 <= k <= len(items):
        recurse(0)
    return result


def power_set(items: list[int]) -> list[list[int]]:
    result: list[list[int]] = []
    chosen: list[int] = []

    def recurse(i: int) -> None:
        if i == len(items):
            result.append(list(chosen))
            return
        recurse(i + 1)  # exclude items[i]
        chosen.append(items[i])
        recurse(i + 1)  # include items[i]
        chosen.pop()

    recurse(0)
    return result


def power_set_bitmask(items: list[int]) -> list[list[int]]:
    n = len(items)
    return [
        [items[i] for i in range(n) if mask >> i & 1]
        for mask in range(1 << n)
    ]


def combinations_bitmask(items: list[int], k: int) -> list[list[int]]:
    """Filter the power set by popcount; simple, but does 2^n work."""
    return [s for s in power_set_bitmask(items) if len(s) == k]


def main() -> None:
    items = [1, 2, 3, 4]
    print(f"C(4,2): {combinations(items, 2)}")
    print(f"C(4,0): {combinations(items, 0)}")
    print(f"C(4,4): {combinations(items, 4)}")
    print(f"C(4,5): {combinations(items, 5)}")

    print(f"power set of [1,2,3]:  {power_set([1, 2, 3])}")
    print(f"bitmask   of [1,2,3]:  {power_set_bitmask([1, 2, 3])}")
    print(f"power set of []:       {power_set([])}")

    same = sorted(combinations(items, 2)) == sorted(combinations_bitmask(items, 2))
    print(f"recursive and bitmask agree for C(4,2): {same}")

    lib = [list(c) for c in it_combinations(items, 2)]
    print(f"itertools C(4,2):      {lib}")
    print(f"matches itertools:     {combinations(items, 2) == lib}")


if __name__ == "__main__":
    main()
