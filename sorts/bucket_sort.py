"""Bucket sort: scatter into range buckets, sort each, concatenate.

Assumes the input is roughly *uniformly distributed* over a known range. Under
that assumption each bucket holds O(1) elements and the total cost is O(n).
Skewed data piles everything into one bucket and it degrades to whatever the
per-bucket sort costs — O(n^2) with insertion sort.

Complexity: O(n + k) average with k buckets, O(n^2) worst. O(n + k) space.
Stable when the per-bucket sort is.
"""


def bucket_sort(values: list[float], bucket_count: int = 10) -> list[float]:
    if not values:
        return []
    lo, hi = min(values), max(values)
    if lo == hi:
        return list(values)

    buckets: list[list[float]] = [[] for _ in range(bucket_count)]
    span = hi - lo
    for v in values:
        # Normalise to [0, 1), then scale — the max lands in the last bucket.
        index = int((v - lo) / span * (bucket_count - 1))
        buckets[index].append(v)

    out: list[float] = []
    for bucket in buckets:
        out.extend(_insertion(bucket))
    return out


def _insertion(a: list[float]) -> list[float]:
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def main() -> None:
    print(bucket_sort([0.42, 0.32, 0.75, 0.12, 0.99, 0.53]))
    print(bucket_sort([29, 25, 3, 49, 9, 37, 21, 43]))
    print(bucket_sort([7, 7, 7]))
    print(bucket_sort([]))


if __name__ == "__main__":
    main()
