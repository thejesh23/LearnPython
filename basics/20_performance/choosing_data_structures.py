"""Choosing the right data structure — usually the biggest speed-up available.

Big-O notation describes how the cost of an operation grows with the size n
of the data. You do not need the maths, just the vocabulary:

    O(1)        constant: same cost for 10 items or 10 million
    O(log n)    tiny growth: a million items needs about 20 steps
    O(n)        linear: twice the data, twice the time
    O(n**2)     quadratic: an O(n) step inside a loop over n items

The costs that matter most day to day:

    x in list             O(n)     x in set / x in dict     O(1)
    list.pop(0)           O(n)     deque.popleft()          O(1)
    list.append / pop()   O(1)     bisect on a sorted list  O(log n)

No micro-optimisation of a loop body competes with replacing an O(n) step by
an O(1) one. The demos print comparisons, not raw timings.
"""

import timeit
from collections.abc import Callable


def best_time(func: Callable[[], object], number: int) -> float:
    return min(timeit.repeat(func, number=number, repeat=5))


def membership_demo() -> None:
    results: dict[str, list[float]] = {"list": [], "set": []}
    for n in (1_000, 10_000):
        items = list(range(n))
        as_set = set(items)
        missing = -1  # worst case for a list: it must check every element
        results["list"].append(best_time(lambda: missing in items, 200))
        results["set"].append(best_time(lambda: missing in as_set, 200))

    list_growth = results["list"][1] / results["list"][0]
    set_growth = results["set"][1] / results["set"][0]
    print("10x more items:")
    print(f"  list lookup became at least 5x slower: {list_growth > 5}")
    print(f"  set lookup stayed about the same (< 3x): {set_growth < 3}")
    print(f"  set beats list at 10,000 items: {results['set'][1] < results['list'][1]}")


def main() -> None:
    membership_demo()


if __name__ == "__main__":
    main()
