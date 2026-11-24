"""Faster Python idioms — and the habit of measuring before believing them.

Python runs your loop body one bytecode instruction at a time, but built-in
functions like `sum`, `min`, `sorted` and `str.join` run their loops in C.
So the classic advice is: push loops into built-ins, avoid doing the same
work twice, and keep hot names local. Some of that advice is worth a lot;
some of it was true in 2010 and barely matters now.

The only reliable guide is a measurement on your Python version, so every
comparison here goes through one helper that

    1. checks both versions give the same answer (a fast wrong answer is a bug)
    2. times both with timeit.repeat and keeps the best round
    3. prints a coarse verdict: "faster" or "slower" only for a gap of at
       least 1.5x either way, otherwise "about the same"

The verdicts are deliberately coarse so they hold on any machine.
"""

import random
import timeit
from collections.abc import Callable


def compare(
    label: str, slow: Callable[[], object], fast: Callable[[], object]
) -> float:
    """Print how `fast` compares with `slow`; return slow_time / fast_time."""
    assert slow() == fast(), f"{label}: the two versions disagree"
    slow_time = min(timeit.repeat(slow, number=20, repeat=5))
    fast_time = min(timeit.repeat(fast, number=20, repeat=5))
    ratio = slow_time / fast_time
    if ratio >= 1.5:
        verdict = "faster"
    elif ratio <= 1 / 1.5:
        verdict = "SLOWER"
    else:
        verdict = "about the same (within 1.5x)"
    print(f"  {label:<34} {verdict}")
    return ratio


RNG = random.Random(42)
NUMBERS = [RNG.randrange(1_000) for _ in range(10_000)]
PIECES = [str(n) for n in NUMBERS]


def manual_total() -> int:
    total = 0
    for n in NUMBERS:
        total += n
    return total


def manual_concat() -> str:
    text = ""
    for piece in PIECES:
        text += piece  # may copy the growing string again and again
    return text


def doubled_with_append() -> list[int]:
    out = []
    for n in NUMBERS:
        out.append(n * 2)
    return out


def builtins_demo() -> None:
    print("idiom versus hand-written loop:")
    compare("sum(NUMBERS) vs a for loop", manual_total, lambda: sum(NUMBERS))
    ratio = compare("''.join vs += in a loop", manual_concat, lambda: "".join(PIECES))
    print(f"  join is faster than +=: {ratio > 1}")
    # A comprehension is a bit quicker than append(), but the real reason to
    # use it is that it is shorter and says what it builds.
    compare("comprehension vs append loop", doubled_with_append,
            lambda: [n * 2 for n in NUMBERS])


def main() -> None:
    builtins_demo()


if __name__ == "__main__":
    main()
