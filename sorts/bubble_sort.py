"""Bubble sort: repeatedly swap adjacent out-of-order pairs.

Each pass "bubbles" the largest remaining element to the end, so after pass i
the last i elements are final. The early-exit flag turns an already-sorted
input into a single O(n) pass.

Complexity: O(n^2) comparisons and swaps worst/average, O(n) best with the
flag. O(1) extra space. Stable. Never use it in production — it is here
because it makes the invariant of a sorting pass obvious.
"""


def bubble_sort(values: list[int]) -> list[int]:
    a = list(values)
    n = len(a)
    for i in range(n - 1):
        swapped = False
        # The tail beyond n-1-i is already in its final position.
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def main() -> None:
    print(bubble_sort([5, 1, 4, 2, 8]))
    print(bubble_sort([1, 2, 3, 4]))
    print(bubble_sort([3, 3, 1]))
    print(bubble_sort([]))


if __name__ == "__main__":
    main()
