"""Adding two numbers stored digit by digit in linked lists.

With the least significant digit first, 342 is 2 -> 4 -> 3, and addition is
exactly the school method: add the two front digits plus the carry, write the
last digit of the sum, carry the rest. The loop continues while either list or
the carry remains, which handles different lengths and a final carry
(5 + 5 = 10 grows a new node) without special cases.

With the most significant digit first the digits come in the wrong order for
carrying. Pushing both lists onto stacks reverses them for free, and building
the answer by prepending puts it back in reading order. Either way the cost is
O(n + m), and the numbers can be far larger than any fixed-width integer.
"""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    next: Node | None = None


def from_int(n: int, little_endian: bool = True) -> Node | None:
    digits = [int(d) for d in str(n)]
    if little_endian:
        digits.reverse()
    head = None
    for d in reversed(digits):
        head = Node(d, head)
    return head


def to_int(head: Node | None, little_endian: bool = True) -> int:
    digits: list[str] = []
    while head:
        digits.append(str(head.value))
        head = head.next
    if little_endian:
        digits.reverse()
    return int("".join(digits) or "0")


def add_little_endian(a: Node | None, b: Node | None) -> Node | None:
    dummy = tail = Node(0)
    carry = 0
    while a or b or carry:
        total = carry + (a.value if a else 0) + (b.value if b else 0)
        carry, digit = divmod(total, 10)
        tail.next = Node(digit)
        tail = tail.next
        a = a.next if a else None
        b = b.next if b else None
    return dummy.next


def add_big_endian(a: Node | None, b: Node | None) -> Node | None:
    xs: list[int] = []
    ys: list[int] = []
    while a:
        xs.append(a.value)
        a = a.next
    while b:
        ys.append(b.value)
        b = b.next
    head, carry = None, 0
    while xs or ys or carry:
        total = carry + (xs.pop() if xs else 0) + (ys.pop() if ys else 0)
        carry, digit = divmod(total, 10)
        head = Node(digit, head)
    return head


def show(head: Node | None) -> str:
    parts: list[str] = []
    while head:
        parts.append(str(head.value))
        head = head.next
    return " -> ".join(parts)


def main() -> None:
    a, b = from_int(342), from_int(465)
    total = add_little_endian(a, b)
    print(f"little endian: {show(a)}  +  {show(b)}  =  {show(total)}")
    print(f"  as integers: 342 + 465 = {to_int(total)}")

    a, b = from_int(7243, False), from_int(564, False)
    total = add_big_endian(a, b)
    print(f"big endian:    {show(a)}  +  {show(b)}  =  {show(total)}")

    print(f"final carry:   5 + 5 = {show(add_little_endian(from_int(5), from_int(5)))}")
    print(f"999 + 1 = {to_int(add_little_endian(from_int(999), from_int(1)))}")

    rng = random.Random(5)
    ok = True
    for _ in range(500):
        x = rng.randrange(10 ** rng.randint(1, 40))
        y = rng.randrange(10 ** rng.randint(1, 40))
        ok &= to_int(add_little_endian(from_int(x), from_int(y))) == x + y
        big = add_big_endian(from_int(x, False), from_int(y, False))
        ok &= to_int(big, little_endian=False) == x + y
    print(f"\nboth orders match int addition on 500 numbers up to 40 digits: {ok}")


if __name__ == "__main__":
    main()
