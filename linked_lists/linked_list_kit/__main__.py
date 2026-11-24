"""Examples and self-check: python3 -m linked_lists.linked_list_kit"""

import heapq
import random
import sys

from . import (
    Node,
    add_numbers,
    find_cycle,
    from_values,
    is_palindrome,
    length,
    merge_k,
    merge_sorted,
    middle,
    reverse,
    reverse_in_groups,
    show,
    to_values,
)


def as_int(head: Node | None) -> int:
    return int("".join(map(str, reversed(to_values(head)))) or "0")


def digits(n: int) -> Node | None:
    return from_values(int(d) for d in reversed(str(n)))


def examples() -> None:
    print("1. reverse:", show(reverse(from_values([1, 2, 3, 4, 5]))))
    print("2. groups of 2:", show(reverse_in_groups(from_values(range(1, 8)), 2)))
    mid = middle(from_values(range(1, 7)))
    print("3. middle of 1..6:", mid.value if mid else None)
    merged = merge_sorted(from_values([1, 4, 9]), from_values([2, 3, 10]))
    print("4. merge:", show(merged))
    print("5. palindrome 1-2-3-2-1:", is_palindrome(from_values([1, 2, 3, 2, 1])))
    print("6. 342 + 465 =", as_int(add_numbers(digits(342), digits(465))))
    nodes = [Node(i) for i in range(6)]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    nodes[-1].next = nodes[2]
    entry, loop = find_cycle(nodes[0])  # type: ignore[misc]
    print(f"7. cycle: enters at {entry.value}, loop length {loop}")


def self_check() -> None:
    rng = random.Random(21)
    for _ in range(400):
        values = [rng.randint(0, 3) for _ in range(rng.randint(0, 12))]
        assert to_values(reverse(from_values(values))) == values[::-1]
        k = rng.randint(1, 5)
        expect = [x for i in range(0, len(values), k)
                  for x in (values[i:i + k][::-1] if i + k <= len(values)
                            else values[i:i + k])]
        assert to_values(reverse_in_groups(from_values(values), k)) == expect
        head = from_values(values)
        assert is_palindrome(head) == (values == values[::-1])
        assert to_values(head) == values, "is_palindrome must restore the list"
        assert length(head) == len(values)
        runs = [sorted(rng.choices(range(50), k=rng.randint(0, 6))) for _ in range(5)]
        merged = merge_k([from_values(r) for r in runs])
        assert to_values(merged) == list(heapq.merge(*runs))
        x, y = rng.randrange(10**15), rng.randrange(10**15)
        assert as_int(add_numbers(digits(x), digits(y))) == x + y
        n = rng.randint(1, 30)
        nodes = [Node(i) for i in range(n)]
        for a, b in zip(nodes, nodes[1:]):
            a.next = b
        entry = rng.choice([None, rng.randrange(n)])
        if entry is None:
            assert find_cycle(nodes[0]) is None
        else:
            nodes[-1].next = nodes[entry]
            assert find_cycle(nodes[0]) == (nodes[entry], n - entry)
    assert reverse(None) is None and middle(None) is None and merge_k([]) is None


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
