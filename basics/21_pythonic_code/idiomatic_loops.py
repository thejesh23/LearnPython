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


def main() -> None:
    enumerate_zip_demo()


if __name__ == "__main__":
    main()
