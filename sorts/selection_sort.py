"""Selection sort: find the minimum of the unsorted tail, swap it into place.

Its distinguishing property is the *number of swaps*: exactly n-1, regardless
of input. That makes it the choice when a write is far more expensive than a
comparison (flash memory, say) — and useless otherwise.

Complexity: O(n^2) comparisons always (no early exit is possible), O(n) swaps,
O(1) space. Not stable in this swap-based form: swapping a[i] with a distant
minimum can jump an equal element past its twin.
"""


def selection_sort(values: list[int]) -> list[int]:
    a = list(values)
    n = len(a)
    for i in range(n - 1):
        smallest = i
        for j in range(i + 1, n):
            if a[j] < a[smallest]:
                smallest = j
        if smallest != i:
            a[i], a[smallest] = a[smallest], a[i]
    return a


def main() -> None:
    print(selection_sort([64, 25, 12, 22, 11]))
    print(selection_sort([1, 2, 3]))
    print(selection_sort([2, 2, 1]))
    print(selection_sort([]))


if __name__ == "__main__":
    main()
