"""`set` — an unordered collection of unique, hashable values.

A set is a dict without the values: O(1) average membership, no duplicates, no
ordering guarantee. Reach for one whenever you are about to write "have I seen
this before?" or "which items are in both lists?".

`{}` is an empty *dict*. The empty set is written `set()`.
"""


def main() -> None:
    s = {3, 1, 4, 1, 5}
    print(f"{{3, 1, 4, 1, 5}} -> {s}   (duplicates dropped, order not kept)")
    print(f"empty set is set(), not {{}}: {type({}).__name__} vs {type(set()).__name__}")

    s.add(9)
    s.discard(100)  # discard is silent; remove would raise
    print(f"after add/discard: {s}, 4 in s -> {4 in s}")

    a = {1, 2, 3, 4}
    b = {3, 4, 5}
    print(f"a | b (union)        = {a | b}")
    print(f"a & b (intersection) = {a & b}")
    print(f"a - b (difference)   = {a - b}")
    print(f"a ^ b (symmetric)    = {a ^ b}")
    print("{1, 2} <= a (subset) =", {1, 2}.issubset(a))
    print(f"a.isdisjoint({{9}})   = {a.isdisjoint({9})}")

    # Deduplicating while keeping first-seen order needs a little help.
    items = ["b", "a", "b", "c", "a"]
    print(f"set(items)        = {set(items)}   (order lost)")
    print(f"dict.fromkeys()   = {list(dict.fromkeys(items))}   (order kept)")

    # Members must be hashable, so no lists inside a set.
    try:
        {[1, 2]}  # type: ignore[misc]
    except TypeError as exc:
        print(f"unhashable: {exc}")

    # frozenset is the immutable version — hashable, so it can live in a set.
    fs = frozenset({1, 2})
    print("set of frozensets:", {fs, frozenset({3})})

    # The reason to bother: membership cost.
    print("list `in`: O(n) scan   |   set `in`: O(1) average hash lookup")


if __name__ == "__main__":
    main()
