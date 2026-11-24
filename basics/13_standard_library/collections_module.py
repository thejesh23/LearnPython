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
from collections import deque
from collections import namedtuple


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


def deque_demo() -> None:
    # list.pop(0) shifts every other element: O(n). deque pops from either
    # end in O(1), which makes it the right type for a queue.
    queue = deque(["first", "second"])
    queue.append("third")          # join at the back
    print(f"served: {queue.popleft()}, waiting: {list(queue)}")

    # maxlen turns a deque into a fixed-size window: old items fall off.
    recent = deque(maxlen=3)
    for reading in [10, 20, 30, 40, 50]:
        recent.append(reading)
    print(f"last three readings: {list(recent)}")

    # rotate(n) moves items from the right end round to the left.
    ring = deque([1, 2, 3, 4, 5])
    ring.rotate(2)
    print(f"rotated by 2: {list(ring)}")


def namedtuple_demo() -> None:
    # point[0] and point[1] say nothing about meaning; point.x and point.y do.
    # A namedtuple is still a tuple: immutable, unpackable, usable as a dict key.
    Point = namedtuple("Point", ["x", "y"])
    p = Point(3, 4)
    print(f"{p}, x = {p.x}, y = {p[1]}")

    x, y = p                       # unpacks like any tuple
    print(f"unpacked: {x}, {y}")

    # Tuples cannot change, so _replace returns a *new* record.
    moved = p._replace(x=10)
    print(f"moved: {moved}, original still {p}")
    print(f"as a dict: {p._asdict()}")
    # For records with defaults, methods or type hints, prefer @dataclass
    # (see basics/09_classes/dataclasses_intro.py).


def main() -> None:
    counter_demo()
    print()
    defaultdict_demo()
    print()
    deque_demo()
    print()
    namedtuple_demo()


if __name__ == "__main__":
    main()
