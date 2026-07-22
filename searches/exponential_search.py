"""Exponential (galloping) search: double the bound, then binary search it.

Probe indices 1, 2, 4, 8, ... until you overshoot the target, then binary
search the last doubled window. Finding the bound costs O(log i) where i is the
answer's index, so the total is O(log i) — better than O(log n) when the target
sits near the front, and it works on an *unbounded* sequence whose length you
cannot ask for.

Timsort uses the same galloping idea to merge runs when one run is consistently
winning.
"""


def exponential_search(values: list[int], target: int) -> int:
    n = len(values)
    if n == 0:
        return -1
    if values[0] == target:
        return 0

    bound = 1
    while bound < n and values[bound] <= target:
        bound *= 2

    lo, hi = bound // 2, min(bound, n - 1)
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if values[mid] == target:
            return mid
        if values[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def search_unbounded(get, target: int) -> int:
    """Search a conceptually infinite sorted sequence via a getter."""
    bound = 1
    while get(bound) < target:
        bound *= 2
    lo, hi = bound // 2, bound
    while lo <= hi:
        mid = (lo + hi) // 2
        value = get(mid)
        if value == target:
            return mid
        if value < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def main() -> None:
    data = list(range(0, 200, 2))
    print(f"search(4)   = {exponential_search(data, 4)}   (near the front: few probes)")
    print(f"search(198) = {exponential_search(data, 198)}")
    print(f"search(5)   = {exponential_search(data, 5)}   (absent)")
    print(f"empty       = {exponential_search([], 1)}")

    # An unbounded sequence: squares, generated on demand.
    print(f"unbounded search for 10_000 in i*i -> index {search_unbounded(lambda i: i * i, 10_000)}")


if __name__ == "__main__":
    main()
