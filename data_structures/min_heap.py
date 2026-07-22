"""Binary min-heap in an array: the parent is never larger than its children.

Index arithmetic replaces pointers: children of i are 2i+1 and 2i+2, the parent
of i is (i-1)//2. Push sifts up, pop moves the last element to the root and
sifts down.

push O(log n), pop O(log n), peek O(1), build-from-list O(n). A heap is only
*partially* ordered — iterating the array is not sorted order.

`heapq` in the standard library is the same structure, in C, and it is what you
should actually use. It is a min-heap only; negate values for a max-heap.
"""

import heapq


class MinHeap:
    def __init__(self, values: list[int] | None = None) -> None:
        self._a: list[int] = list(values or [])
        for i in range(len(self._a) // 2 - 1, -1, -1):  # O(n) heapify
            self._sift_down(i)

    def push(self, value: int) -> None:
        self._a.append(value)
        self._sift_up(len(self._a) - 1)

    def pop(self) -> int:
        if not self._a:
            raise IndexError("pop from empty heap")
        top = self._a[0]
        last = self._a.pop()
        if self._a:
            self._a[0] = last
            self._sift_down(0)
        return top

    def peek(self) -> int:
        return self._a[0]

    def _sift_up(self, i: int) -> None:
        while i > 0:
            parent = (i - 1) // 2
            if self._a[i] >= self._a[parent]:
                break
            self._a[i], self._a[parent] = self._a[parent], self._a[i]
            i = parent

    def _sift_down(self, i: int) -> None:
        n = len(self._a)
        while True:
            smallest = i
            for child in (2 * i + 1, 2 * i + 2):
                if child < n and self._a[child] < self._a[smallest]:
                    smallest = child
            if smallest == i:
                return
            self._a[i], self._a[smallest] = self._a[smallest], self._a[i]
            i = smallest

    def __len__(self) -> int:
        return len(self._a)


def k_smallest(values: list[int], k: int) -> list[int]:
    """A max-heap of size k: O(n log k), better than sorting when k << n."""
    heap: list[int] = []
    for value in values:
        heapq.heappush(heap, -value)
        if len(heap) > k:
            heapq.heappop(heap)
    return sorted(-v for v in heap)


def main() -> None:
    heap = MinHeap([5, 3, 8, 1, 9])
    print(f"peek: {heap.peek()}")
    print(f"drained in order: {[heap.pop() for _ in range(len(heap))]}")

    heap = MinHeap()
    for v in (4, 2, 7):
        heap.push(v)
    print(f"after pushes, min = {heap.peek()}")

    # heapq: the version to use.
    hq = [5, 3, 8, 1]
    heapq.heapify(hq)
    heapq.heappush(hq, 0)
    print(f"heapq pop: {heapq.heappop(hq)}, array is only partially ordered: {hq}")
    print(f"nsmallest: {heapq.nsmallest(3, [5, 1, 9, 3, 7])}")
    print(f"nlargest:  {heapq.nlargest(2, [5, 1, 9, 3, 7])}")
    print(f"k_smallest(3): {k_smallest([9, 4, 7, 1, 8, 2], 3)}")
    print(f"merge sorted streams: {list(heapq.merge([1, 4], [2, 3], [5]))}")


if __name__ == "__main__":
    main()
