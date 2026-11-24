"""Idiomatic loops — before/after pairs that say what they mean.

Python's `for` loop walks over *things*, not over index numbers. Code that
reaches for `range(len(...))` and a manual counter usually has a clearer
version built from a few helpers:

    enumerate(xs)        the item AND its position
    zip(a, b)            walk two sequences side by side
    d.items()            keys and values together
    any / all / sum      a whole loop that answers one question
    a, *rest = ...       unpacking instead of indexing

Each demo below runs a "before" and an "after" version of the same task and
checks they agree. The after version is shorter, but more importantly it is
harder to get wrong: there is no index to be off by one.
"""


PLAYERS = ["ana", "ben", "cho"]
SCORES = [31, 47, 25]


def ranking_before() -> list[str]:
    lines = []
    for i in range(len(PLAYERS)):  # an index just to reach two lists
        lines.append(f"{i + 1}. {PLAYERS[i]} {SCORES[i]}")
    return lines


def ranking_after() -> list[str]:
    # zip pairs the lists; enumerate counts, starting wherever you ask.
    # strict=True raises if the lists have different lengths, instead of
    # silently stopping at the shorter one.
    return [
        f"{rank}. {name} {score}"
        for rank, (name, score) in enumerate(zip(PLAYERS, SCORES, strict=True), 1)
    ]


def enumerate_zip_demo() -> None:
    print(f"same result: {ranking_before() == ranking_after()}")
    for line in ranking_after():
        print(f"  {line}")
    try:
        list(zip(PLAYERS, SCORES[:2], strict=True))
    except ValueError as exc:
        print(f"zip(strict=True) caught a mismatch: {exc}")


STOCK = {"apples": 12, "pears": 0, "plums": 7}


def report_before() -> list[str]:
    out = []
    keys = list(STOCK.keys())
    keys.sort()
    for k in keys:
        out.append(f"{k}={STOCK[k]}")  # a second lookup for every key
    return out


def report_after() -> list[str]:
    return [f"{name}={count}" for name, count in sorted(STOCK.items())]


def dict_items_demo() -> None:
    print(f"same result: {report_before() == report_after()}")
    print(f"  {', '.join(report_after())}")
    # Sorting by value instead of key: pass a key function.
    by_count = sorted(STOCK.items(), key=lambda pair: pair[1], reverse=True)
    print(f"  most stocked first: {by_count}")
    # Iterating a dict gives its keys, so `.keys()` is rarely needed.
    print(f"  'pears' in STOCK: {'pears' in STOCK}")


ORDERS = [
    {"id": 1, "total": 40.0, "paid": True},
    {"id": 2, "total": 15.5, "paid": False},
    {"id": 3, "total": 99.9, "paid": True},
]


def summary_before() -> tuple[bool, bool, float, int]:
    has_unpaid = False
    for order in ORDERS:
        if not order["paid"]:
            has_unpaid = True
            break
    all_positive = True
    for order in ORDERS:
        if order["total"] <= 0:
            all_positive = False
    revenue = 0.0
    for order in ORDERS:
        if order["paid"]:
            revenue += order["total"]
    biggest = ORDERS[0]
    for order in ORDERS:
        if order["total"] > biggest["total"]:
            biggest = order
    return has_unpaid, all_positive, revenue, biggest["id"]


def summary_after() -> tuple[bool, bool, float, int]:
    # Each loop above answered one question; each line below names it.
    has_unpaid = any(not o["paid"] for o in ORDERS)  # stops at first True
    all_positive = all(o["total"] > 0 for o in ORDERS)  # stops at first False
    revenue = sum(o["total"] for o in ORDERS if o["paid"])
    biggest = max(ORDERS, key=lambda o: o["total"])
    return has_unpaid, all_positive, revenue, biggest["id"]


def any_all_sum_demo() -> None:
    print(f"same result: {summary_before() == summary_after()}")
    has_unpaid, all_positive, revenue, biggest = summary_after()
    print(f"  unpaid orders: {has_unpaid}, all positive: {all_positive}")
    print(f"  paid revenue: {revenue}, biggest order id: {biggest}")
    # Edge cases worth knowing: any([]) is False, all([]) is True.
    print(f"  any([]) = {any([])}, all([]) = {all([])}")


def main() -> None:
    enumerate_zip_demo()
    print()
    dict_items_demo()
    print()
    any_all_sum_demo()


if __name__ == "__main__":
    main()
