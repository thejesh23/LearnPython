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


def main() -> None:
    counter_demo()


if __name__ == "__main__":
    main()
