"""`collections` — specialised containers that replace hand-written bookkeeping.

The built-in list, dict and set cover most needs. `collections` adds a few
containers for patterns that come up constantly:

    Counter      counting things (a dict of item -> count)
    defaultdict  a dict that creates missing values for you
    deque        a list with fast appends and pops at *both* ends
    namedtuple   a tuple whose fields also have names

Each one removes a few lines of fiddly code, and the bugs that hide in them.
"""

from collections import Counter
from collections import defaultdict


def counter_demo() -> None:
    # Counting by hand means "if key in d: d[key] += 1 else: d[key] = 1".
    # Counter does it in one call, and a missing key simply counts as 0.
    words = "the cat and the hat and the bat".split()
    counts = Counter(words)
    print(f"counts: {counts}")
    print(f"'the' appears {counts['the']} times, 'dog' {counts['dog']} times")

    # most_common(n) returns the n biggest counts, largest first.
    print(f"top two: {counts.most_common(2)}")

    # Counters add and subtract like multisets; negative results are dropped.
    have = Counter(apples=3, pears=1)
    need = Counter(apples=1, pears=2)
    print(f"have - need = {have - need}  (pears would go negative, so vanish)")
    print(f"have + need = {have + need}")


def defaultdict_demo() -> None:
    # defaultdict(list) calls list() to make a fresh value the first time a
    # key is used, so grouping needs no "if key not in d" check.
    animals = ["cat", "cow", "dog", "duck", "camel"]
    by_letter: defaultdict[str, list[str]] = defaultdict(list)
    for name in animals:
        by_letter[name[0]].append(name)
    print(f"grouped: {dict(by_letter)}")

    # Any zero-argument callable works as the factory: int gives 0, set gives set().
    lengths: defaultdict[int, set[str]] = defaultdict(set)
    for name in animals:
        lengths[len(name)].add(name)
    print(f"by length: {dict(sorted(lengths.items()))}")

    # Careful: merely *reading* a missing key creates it.
    _ = by_letter["z"]
    print(f"after reading 'z': 'z' in by_letter -> {'z' in by_letter}")


def main() -> None:
    counter_demo()
    print()
    defaultdict_demo()


if __name__ == "__main__":
    main()
