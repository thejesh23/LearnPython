"""Merge sort: split in half, sort each half, merge the two sorted runs.

The merge step is the whole algorithm — it walks both halves with two pointers
and always takes the smaller head. Taking from the left half on ties is what
makes the sort stable.

Complexity: O(n log n) in every case, O(n) extra space. The guaranteed bound
and the stability are why it underpins Timsort and every external (on-disk)
sort.
"""


def merge_sort(values: list[int]) -> list[int]:
    if len(values) <= 1:
        return list(values)
    mid = len(values) // 2
    left = merge_sort(values[:mid])
    right = merge_sort(values[mid:])
    return merge(left, right)


def merge(left: list[int], right: list[int]) -> list[int]:
    out: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # <= keeps equal elements in original order
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def merge_sort_bottom_up(values: list[int]) -> list[int]:
    """The same algorithm without recursion: merge runs of 1, then 2, 4, ..."""
    a = list(values)
    width = 1
    while width < len(a):
        for lo in range(0, len(a), 2 * width):
            mid, hi = lo + width, min(lo + 2 * width, len(a))
            a[lo:hi] = merge(a[lo:mid], a[mid:hi])
        width *= 2
    return a


def main() -> None:
    print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
    print(merge_sort_bottom_up([38, 27, 43, 3, 9, 82, 10]))
    print(merge([1, 3, 5], [2, 4]))
    print(merge_sort([]))


if __name__ == "__main__":
    main()
