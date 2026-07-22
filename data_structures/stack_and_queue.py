"""Stack and queue — and which Python type to build them on.

A stack is a plain `list`: append/pop at the end are both amortised O(1).

A queue is *not* a plain list. `list.pop(0)` shifts every remaining element,
so it is O(n) and a loop over it is quadratic. Use `collections.deque`, which
is a doubly linked list of blocks with O(1) at both ends.

`queue.Queue` is a different thing again: a thread-safe queue with blocking
`get`, meant for handing work between threads, not for algorithms.
"""

import time
from collections import deque


class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> T:
        return self._items[-1]

    def __len__(self) -> int:
        return len(self._items)


class Queue[T]:
    def __init__(self) -> None:
        self._items: deque[T] = deque()

    def enqueue(self, item: T) -> None:
        self._items.append(item)

    def dequeue(self) -> T:
        if not self._items:
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()  # O(1), unlike list.pop(0)

    def __len__(self) -> int:
        return len(self._items)


class MinStack:
    """Stack that also reports its minimum in O(1), by stacking minima too."""

    def __init__(self) -> None:
        self._items: list[int] = []
        self._mins: list[int] = []

    def push(self, value: int) -> None:
        self._items.append(value)
        self._mins.append(value if not self._mins else min(value, self._mins[-1]))

    def pop(self) -> int:
        self._mins.pop()
        return self._items.pop()

    def minimum(self) -> int:
        return self._mins[-1]


def main() -> None:
    stack = Stack[int]()
    for n in (1, 2, 3):
        stack.push(n)
    print(f"stack pop {stack.pop()}, peek {stack.peek()}, len {len(stack)}")

    q = Queue[str]()
    for item in ("a", "b", "c"):
        q.enqueue(item)
    print(f"queue dequeue {q.dequeue()}, then {q.dequeue()}, len {len(q)}")

    ms = MinStack()
    for n in (5, 3, 7, 2):
        ms.push(n)
    print(f"min {ms.minimum()}, pop {ms.pop()}, min now {ms.minimum()}")

    # Why deque: measured.
    n = 50_000
    start = time.perf_counter()
    lst = list(range(n))
    while lst:
        lst.pop(0)
    list_time = time.perf_counter() - start

    start = time.perf_counter()
    dq = deque(range(n))
    while dq:
        dq.popleft()
    deque_time = time.perf_counter() - start
    print(f"drain {n} items: list.pop(0) {list_time:.3f}s vs deque.popleft {deque_time:.4f}s")


if __name__ == "__main__":
    main()
