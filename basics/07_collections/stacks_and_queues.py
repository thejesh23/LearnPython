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


def main() -> None:
    stack_demo()


if __name__ == "__main__":
    main()
