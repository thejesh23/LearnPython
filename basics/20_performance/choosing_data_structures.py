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
from collections import deque
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


def drain_list(n: int) -> int:
    queue = list(range(n))
    total = 0
    while queue:
        total += queue.pop(0)  # shifts every remaining item left: O(n)
    return total


def drain_deque(n: int) -> int:
    queue = deque(range(n))
    total = 0
    while queue:
        total += queue.popleft()  # O(1): a deque is built for both ends
    return total


def queue_demo() -> None:
    n = 50_000
    print(f"same total: {drain_list(n) == drain_deque(n)}")
    list_time = best_time(lambda: drain_list(n), 1)
    deque_time = best_time(lambda: drain_deque(n), 1)
    print(f"deque.popleft faster than list.pop(0): {deque_time < list_time}")
    # Popping from the END of a list is O(1), so a list is a fine stack.
    stack = [1, 2, 3]
    print(f"list as a stack (pop from the end): {stack.pop()}, {stack.pop()}")


USERS = [{"id": i, "name": f"user{i}"} for i in range(5_000)]
WANTED = list(range(0, 5_000, 50))  # 100 ids to look up


def names_by_scanning() -> list[str]:
    # For each wanted id, walk the list: O(n) per lookup, O(n * m) in total.
    return [next(u["name"] for u in USERS if u["id"] == i) for i in WANTED]


def names_by_index() -> list[str]:
    # Build an id -> user dict once (O(n)), then each lookup is O(1).
    by_id = {u["id"]: u for u in USERS}
    return [by_id[i]["name"] for i in WANTED]


def dict_index_demo() -> None:
    print(f"same names: {names_by_scanning() == names_by_index()}")
    scan = best_time(names_by_scanning, 3)
    index = best_time(names_by_index, 3)
    print(f"index (including building it) faster than scanning: {index < scan}")
    # Rule of thumb: if you search the same list more than a few times,
    # build a dict (or set) from it first.


def main() -> None:
    membership_demo()
    print()
    queue_demo()
    print()
    dict_index_demo()


if __name__ == "__main__":
    main()
