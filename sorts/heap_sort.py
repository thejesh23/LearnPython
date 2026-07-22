"""Heap sort: build a max-heap in the array, then repeatedly extract the max.

A binary heap stored in an array needs no pointers: the children of i sit at
2i+1 and 2i+2. Building the heap bottom-up with sift-down is O(n), not
O(n log n) — the deep nodes, which are numerous, barely move.

Complexity: O(n log n) worst case with O(1) extra space — the only common sort
with both. Not stable, and its cache behaviour is poor, which is why quicksort
usually wins in practice.
"""


def heap_sort(values: list[int]) -> list[int]:
    a = list(values)
    n = len(a)
    # Heapify: sift down every internal node, from the last one up.
    for start in range(n // 2 - 1, -1, -1):
        _sift_down(a, start, n)
    # Extract: swap the max to the end, shrink the heap, restore the invariant.
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        _sift_down(a, 0, end)
    return a


def _sift_down(a: list[int], root: int, size: int) -> None:
    while True:
        largest = root
        left, right = 2 * root + 1, 2 * root + 2
        if left < size and a[left] > a[largest]:
            largest = left
        if right < size and a[right] > a[largest]:
            largest = right
        if largest == root:
            return
        a[root], a[largest] = a[largest], a[root]
        root = largest


def heap_sort_stdlib(values: list[int]) -> list[int]:
    """The standard library's heapq is a *min*-heap over a plain list."""
    import heapq

    heap = list(values)
    heapq.heapify(heap)  # O(n)
    return [heapq.heappop(heap) for _ in range(len(heap))]


def main() -> None:
    print(heap_sort([4, 10, 3, 5, 1]))
    print(heap_sort([1]))
    print(heap_sort_stdlib([4, 10, 3, 5, 1]))
    print(heap_sort([]))


if __name__ == "__main__":
    main()
