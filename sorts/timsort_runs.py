"""Timsort's core idea: find natural runs, extend them, merge them.

CPython's `list.sort()` is Timsort. It is an adaptive merge sort built on one
observation: real data is full of already-ordered stretches. Timsort finds
those runs, reverses descending ones in place, pads short runs to a minimum
length with binary insertion sort, and merges runs under invariants that keep
the merge tree balanced.

This file implements the run-detection and merging skeleton — enough to see why
`sorted()` is O(n) on sorted input and never worse than O(n log n).
"""


def find_runs(a: list[int]) -> list[tuple[int, int]]:
    """Split the array into maximal ascending runs (descending ones reversed)."""
    runs: list[tuple[int, int]] = []
    i, n = 0, len(a)
    while i < n:
        start = i
        i += 1
        if i == n:
            runs.append((start, i))
            break
        if a[i] < a[i - 1]:  # descending run
            while i < n and a[i] < a[i - 1]:
                i += 1
            a[start:i] = reversed(a[start:i])  # in place, keeps it stable
        else:  # ascending (non-decreasing) run
            while i < n and a[i] >= a[i - 1]:
                i += 1
        runs.append((start, i))
    return runs


def min_run_length(n: int) -> int:
    """CPython picks 32..64 so that n/minrun is at or just below a power of 2."""
    r = 0
    while n >= 64:
        r |= n & 1
        n >>= 1
    return n + r


def timsort(values: list[int]) -> list[int]:
    a = list(values)
    minrun = min_run_length(len(a))
    result: list[int] = []
    for start, end in find_runs(a):
        run = a[start:end]
        # Extend a short run with binary insertion sort, as Timsort does.
        while len(run) < minrun and end < len(a):
            _insort(run, a[end])
            end += 1
        result = _merge(result, run) if result else run
    return result


def _insort(run: list[int], value: int) -> None:
    lo, hi = 0, len(run)
    while lo < hi:
        mid = (lo + hi) // 2
        if run[mid] <= value:
            lo = mid + 1
        else:
            hi = mid
    run.insert(lo, value)


def _merge(left: list[int], right: list[int]) -> list[int]:
    out: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def main() -> None:
    data = [5, 6, 7, 1, 2, 9, 8, 7, 3]
    print(f"runs in {data}: {find_runs(list(data))}")
    print(f"minrun(1000) = {min_run_length(1000)}")
    print(timsort(data))
    print(timsort(list(range(10))))
    print(timsort([]))


if __name__ == "__main__":
    main()
