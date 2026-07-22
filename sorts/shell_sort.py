"""Shell sort: insertion sort on gapped subsequences, with a shrinking gap.

Insertion sort only ever moves an element one position at a time, so a small
value stranded at the far right costs O(n) moves. Shell sort fixes that by
first sorting elements that are `gap` apart, which moves things a long way
cheaply, then shrinking the gap until it reaches 1 — where the array is nearly
sorted and insertion sort is fast.

Complexity depends entirely on the gap sequence: O(n^2) with Shell's original
halving, O(n^1.5) with Knuth's 3k+1, O(n^(4/3)) with Sedgewick's. O(1) space,
not stable.
"""


def shell_sort(values: list[int]) -> list[int]:
    a = list(values)
    n = len(a)
    # Knuth's sequence: 1, 4, 13, 40, ... built up below n/3.
    gap = 1
    while gap < n // 3:
        gap = 3 * gap + 1
    while gap >= 1:
        for i in range(gap, n):
            key = a[i]
            j = i
            while j >= gap and a[j - gap] > key:
                a[j] = a[j - gap]
                j -= gap
            a[j] = key
        gap //= 3
    return a


def shell_sort_halving(values: list[int]) -> list[int]:
    """Shell's original gaps (n/2, n/4, ...): simpler, measurably worse."""
    a = list(values)
    gap = len(a) // 2
    while gap > 0:
        for i in range(gap, len(a)):
            key, j = a[i], i
            while j >= gap and a[j - gap] > key:
                a[j] = a[j - gap]
                j -= gap
            a[j] = key
        gap //= 2
    return a


def main() -> None:
    print(shell_sort([23, 12, 1, 8, 34, 54, 2, 3]))
    print(shell_sort_halving([23, 12, 1, 8, 34, 54, 2, 3]))
    print(shell_sort([5, 4, 3, 2, 1]))
    print(shell_sort([]))


if __name__ == "__main__":
    main()
