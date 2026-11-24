"""Stacks, queues and priority queues with list, deque and heapq.

Three ways to hold "work waiting to be done", which differ only in what comes
out next:

    stack           last in, first out (LIFO)     list: append / pop
    queue           first in, first out (FIFO)    collections.deque: append / popleft
    priority queue  smallest first                heapq on a plain list

A list is a fine stack because both operations happen at the end, which is
cheap. It is a poor queue: `list.pop(0)` shifts every remaining item left, so
it gets slower as the list grows. `deque` pops from either end in constant
time. A heap keeps the smallest item at index 0 and reorders only a few items
per push or pop, which is much cheaper than sorting the whole list each time.

For queues shared between threads, use queue.Queue, which adds locking.
"""

import timeit
from collections import deque


PAIRS = {")": "(", "]": "[", "}": "{"}


def is_balanced(text: str) -> bool:
    """Every closing bracket must match the most recent unmatched opener."""
    stack: list[str] = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)  # push
        elif ch in PAIRS:
            if not stack or stack.pop() != PAIRS[ch]:  # pop the latest opener
                return False
    return not stack  # leftovers mean something was never closed


def stack_demo() -> None:
    for text in ["(a[b]{c})", "(]", "((x)", "f(g[0], {1: 2})"]:
        print(f"{text!r:<20} balanced? {is_balanced(text)}")

    # Undo history: the last change made is the first one undone.
    history: list[str] = []
    for action in ["type 'hi'", "bold", "delete word"]:
        history.append(action)
    print(f"history: {history}")
    print(f"undo -> {history.pop()}")
    print(f"undo -> {history.pop()}")
    print(f"peek at top without removing: {history[-1]!r}")


GRID = [
    "S.#.....",
    ".##.###.",
    "....#...",
    ".##...#E",
]


def shortest_path_length(grid: list[str]) -> int:
    """Breadth-first search: explore cells in the order they were discovered."""
    rows, cols = len(grid), len(grid[0])
    start = next((r, c) for r in range(rows) for c in range(cols) if grid[r][c] == "S")
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        (r, c), steps = queue.popleft()  # oldest first: that is what makes it FIFO
        if grid[r][c] == "E":
            return steps
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                if (nr, nc) not in seen:
                    seen.add((nr, nc))
                    queue.append(((nr, nc), steps + 1))
    return -1


def queue_demo() -> None:
    line = deque(["ada", "alan"])
    line.append("grace")  # join at the back
    print(f"served {line.popleft()}, then {line.popleft()}, waiting: {list(line)}")

    print("\n".join(GRID))
    print(f"shortest path S -> E: {shortest_path_length(GRID)} steps")

    # Draining 20,000 items from the front: list.pop(0) vs deque.popleft().
    n = 20_000
    list_time = timeit.timeit(
        "while q: q.pop(0)", setup=f"q = list(range({n}))", number=1
    )
    deque_time = timeit.timeit(
        "while q: q.popleft()",
        setup=f"from collections import deque; q = deque(range({n}))",
        number=1,
    )
    print(f"deque.popleft() faster than list.pop(0): {deque_time < list_time}")


def main() -> None:
    stack_demo()
    print()
    queue_demo()


if __name__ == "__main__":
    main()
