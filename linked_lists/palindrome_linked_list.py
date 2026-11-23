"""Is a singly linked list a palindrome, in O(1) extra space?

Copying the values into a Python list and comparing with its reverse is O(n)
space and perfectly fine in practice. The constant-space version is the one
that teaches pointer work:

1. find the middle with slow and fast pointers;
2. reverse the second half in place;
3. walk both halves together, comparing values;
4. reverse the second half again so the caller's list is left intact.

Step 4 is the one people skip. A function called is_palindrome should not
quietly scramble its argument, and the demo checks that it does not.
"""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    next: Node | None = None


def build(values: list[int]) -> Node | None:
    head = None
    for v in reversed(values):
        head = Node(v, head)
    return head


def to_list(head: Node | None) -> list[int]:
    out: list[int] = []
    while head:
        out.append(head.value)
        head = head.next
    return out


def reverse(head: Node | None) -> Node | None:
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev


def is_palindrome(head: Node | None) -> bool:
    if head is None or head.next is None:
        return True
    slow = fast = head
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next  # type: ignore[assignment]
    second = reverse(slow.next)
    left, right, result = head, second, True
    while right:
        if left.value != right.value:  # type: ignore[union-attr]
            result = False
            break
        left, right = left.next, right.next  # type: ignore[union-attr]
    slow.next = reverse(second)  # restore the caller's list
    return result


def is_palindrome_copy(head: Node | None) -> bool:
    values = to_list(head)
    return values == values[::-1]


def main() -> None:
    for values in [[1, 2, 2, 1], [1, 2, 3, 2, 1], [1, 2], [7], [], [1, 2, 3, 1]]:
        head = build(values)
        answer = is_palindrome(head)
        intact = to_list(head) == values
        print(f"{str(values):<17} palindrome: {answer!s:<5} list intact: {intact}")

    rng = random.Random(11)
    ok = True
    for _ in range(1000):
        half = rng.choices(range(3), k=rng.randint(0, 5))
        values = half + rng.choices(range(3), k=rng.randint(0, 1)) + half[::-1]
        if rng.random() < 0.5:
            values = rng.choices(range(3), k=rng.randint(0, 8))
        head = build(values)
        ok &= is_palindrome(head) == is_palindrome_copy(head)
        ok &= to_list(head) == values
    print(f"\nagrees with the copy version and restores the list (1000 cases): {ok}")


if __name__ == "__main__":
    main()
