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


def main() -> None:
    enumerate_zip_demo()
    print()
    dict_items_demo()


if __name__ == "__main__":
    main()
