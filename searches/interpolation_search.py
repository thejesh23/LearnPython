"""Interpolation search: guess where the value *should* be, not the midpoint.

Binary search always probes the middle. Interpolation search assumes the data
is roughly uniformly distributed and probes proportionally — looking for 950 in
1..1000 it jumps straight near the end, the way you open a phone book.

Complexity: O(log log n) on uniform data, but O(n) when the distribution is
skewed (exponentially growing values, say). The guard below keeps it from
probing outside the range.
"""


def interpolation_search(values: list[int], target: int) -> int:
    lo, hi = 0, len(values) - 1
    while lo <= hi and values[lo] <= target <= values[hi]:
        if values[lo] == values[hi]:  # flat range: avoid dividing by zero
            return lo if values[lo] == target else -1
        # Linear interpolation between the two endpoints.
        pos = lo + (target - values[lo]) * (hi - lo) // (values[hi] - values[lo])
        if values[pos] == target:
            return pos
        if values[pos] < target:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1


def main() -> None:
    uniform = list(range(0, 1000, 10))
    print(f"uniform: search(950) = {interpolation_search(uniform, 950)}")
    print(f"uniform: search(0)   = {interpolation_search(uniform, 0)}")
    print(f"uniform: search(955) = {interpolation_search(uniform, 955)}  (absent)")

    skewed = [1, 2, 4, 8, 16, 32, 64, 128, 100_000]
    print(f"skewed:  search(64)  = {interpolation_search(skewed, 64)}")
    print("on skewed data the probe is a poor guess and it degrades to O(n)")

    print(f"flat:    search(5) in [5,5,5] = {interpolation_search([5, 5, 5], 5)}")
    print(f"empty:   {interpolation_search([], 1)}")


if __name__ == "__main__":
    main()
