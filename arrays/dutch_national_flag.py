"""Dutch national flag: partition into three groups in a single pass.

Dijkstra's problem — sort an array of three distinct values (0/1/2, or
red/white/blue). Three pointers maintain four regions:

    [0, low)      known 0s
    [low, mid)    known 1s
    [mid, high]   unclassified
    (high, n)     known 2s

Swapping from the back does not advance `mid`, because the value swapped in is
still unclassified. That asymmetry is the whole trick.

O(n) time, O(1) space. Also the three-way partition that makes quicksort fast
on inputs with many duplicate keys.
"""


def dutch_flag_sort(values: list[int]) -> list[int]:
    a = list(values)
    low, mid, high = 0, 0, len(a) - 1
    while mid <= high:
        if a[mid] == 0:
            a[low], a[mid] = a[mid], a[low]
            low += 1
            mid += 1
        elif a[mid] == 1:
            mid += 1
        else:  # a[mid] == 2
            a[mid], a[high] = a[high], a[mid]
            high -= 1  # mid is NOT advanced
    return a


def three_way_partition(values: list[int], pivot: int) -> list[int]:
    """The generalisation: < pivot, == pivot, > pivot."""
    a = list(values)
    low, mid, high = 0, 0, len(a) - 1
    while mid <= high:
        if a[mid] < pivot:
            a[low], a[mid] = a[mid], a[low]
            low += 1
            mid += 1
        elif a[mid] == pivot:
            mid += 1
        else:
            a[mid], a[high] = a[high], a[mid]
            high -= 1
    return a


def main() -> None:
    print(dutch_flag_sort([2, 0, 2, 1, 1, 0]))
    print(dutch_flag_sort([0, 0, 0]))
    print(three_way_partition([9, 3, 5, 5, 1, 7, 5], 5))


if __name__ == "__main__":
    main()
