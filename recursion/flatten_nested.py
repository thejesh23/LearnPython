"""Flattening arbitrarily nested lists into a single flat sequence.

The recursive version is a direct reading of the data's shape: walk the items,
and if an item is itself a list, flatten it and splice the result in, otherwise
emit it. The recursion depth equals the nesting depth, not the number of
elements, which is usually small — but "usually" is doing real work there.

Python has no tail-call optimisation and a default recursion limit near 1000,
so a list nested a few thousand deep raises RecursionError. The fix is an
explicit stack: push the top-level list, pop items, and push sub-lists back for
later. The stack lives on the heap, so depth is bounded by memory instead of by
the interpreter's frame limit.

Both are O(n) in the total number of leaves and interior nodes. The iterative
version below reverses each sub-list when pushing so that popping restores the
original left-to-right order.
"""

import sys
from typing import Any


def flatten(nested: list[Any]) -> list[Any]:
    out: list[Any] = []
    for item in nested:
        if isinstance(item, list):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out


def flatten_iterative(nested: list[Any]) -> list[Any]:
    out: list[Any] = []
    stack: list[Any] = list(reversed(nested))
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(reversed(item))  # reversed so pops come out in order
        else:
            out.append(item)
    return out


def flatten_lazy(nested: list[Any]) -> Any:
    """A generator: yields leaves one at a time without building a list."""
    for item in nested:
        if isinstance(item, list):
            yield from flatten_lazy(item)
        else:
            yield item


def deeply_nested(depth: int) -> list[Any]:
    node: list[Any] = [depth]
    for i in range(depth - 1, 0, -1):
        node = [i, node]
    return node


def main() -> None:
    data = [1, [2, [3, [4, 5]], 6], [], [[7], 8]]
    print(f"recursive: {flatten(data)}")
    print(f"iterative: {flatten_iterative(data)}")
    print(f"generator: {list(flatten_lazy(data))}")

    print(f"empty:        {flatten([])}")
    print(f"only empties: {flatten([[], [[]], [[], []]])}")
    print(f"mixed types:  {flatten([1, ['a', [None, True]], 2.5])}")

    print(f"recursion limit: {sys.getrecursionlimit()}")
    deep = deeply_nested(5000)
    try:
        flatten(deep)
    except RecursionError:
        print("recursive flatten on depth 5000: RecursionError")
    flat = flatten_iterative(deep)
    print(f"iterative flatten on depth 5000: {len(flat)} leaves, "
          f"first {flat[0]}, last {flat[-1]}")


if __name__ == "__main__":
    main()
