"""Ternary search: find the extremum of a unimodal function.

Not a replacement for binary search on sorted arrays (it makes more
comparisons for the same job). Its real use is optimisation: given a function
that rises then falls (unimodal), two probes per iteration tell you which third
of the range cannot contain the peak.

Complexity: O(log n) iterations, each discarding one third of the range.
For continuous domains, iterate a fixed number of times or until the interval
is smaller than the tolerance you need.
"""


def ternary_search_max(f, lo: float, hi: float, iterations: int = 200) -> float:
    """Return the argmax of a unimodal f on [lo, hi]."""
    for _ in range(iterations):
        third = (hi - lo) / 3
        m1, m2 = lo + third, hi - third
        if f(m1) < f(m2):
            lo = m1  # the peak cannot be left of m1
        else:
            hi = m2
    return (lo + hi) / 2


def ternary_search_peak_index(values: list[int]) -> int:
    """Index of the peak in a strictly increasing-then-decreasing list."""
    lo, hi = 0, len(values) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] < values[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo


def main() -> None:
    # A downward parabola peaking at x = 3.
    peak = ternary_search_max(lambda x: -((x - 3) ** 2) + 10, -10, 10)
    print(f"argmax of -(x-3)^2 + 10 -> {peak:.6f}")

    mountain = [1, 3, 8, 12, 4, 2]
    idx = ternary_search_peak_index(mountain)
    print(f"peak of {mountain} at index {idx} (value {mountain[idx]})")

    # Minimising works the same way with the comparison flipped.
    trough = ternary_search_max(lambda x: -abs(x + 2), -10, 10)
    print(f"argmin of |x+2| -> {trough:.6f}")


if __name__ == "__main__":
    main()
