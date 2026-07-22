"""`range`, `enumerate`, `zip`, `reversed` — the loop helpers.

`range(start, stop, step)` follows the same half-open convention as slicing:
stop is excluded. It is *lazy* — `range(10**9)` allocates almost nothing,
because it computes each value on demand rather than building a list.

The others are lazy too: they hand back iterators, so wrap them in `list()`
when you want to see or reuse the values.
"""


def main() -> None:
    print(f"range(5)        -> {list(range(5))}")
    print(f"range(2, 6)     -> {list(range(2, 6))}")
    print(f"range(0, 10, 3) -> {list(range(0, 10, 3))}")
    print(f"range(5, 0, -1) -> {list(range(5, 0, -1))}")
    print(f"range(5) is lazy: {range(5)!r}, len={len(range(5))}, 3 in it -> {3 in range(5)}")

    # A billion-element range costs nothing until you iterate it.
    huge = range(10**9)
    print(f"huge[999_999] = {huge[999_999]}  (computed, not stored)")

    # enumerate replaces `for i in range(len(xs))`.
    xs = ["a", "b", "c"]
    for i, x in enumerate(xs):
        print(f"{i}: {x}")
    print(f"enumerate(xs, 1) -> {list(enumerate(xs, start=1))}")

    # zip pairs sequences; zip(*pairs) unzips them again.
    pairs = list(zip("abc", [1, 2, 3]))
    print(f"zip -> {pairs}")
    letters, numbers = zip(*pairs)
    print(f"unzipped -> {letters} {numbers}")
    # strict=True (3.10+) raises instead of silently truncating.
    try:
        list(zip([1, 2, 3], [1, 2], strict=True))
    except ValueError as exc:
        print(f"zip strict: {exc}")

    # reversed and sorted round out the set.
    print(f"reversed -> {list(reversed(xs))}")
    print(f"sorted by length -> {sorted(['ccc', 'a', 'bb'], key=len)}")

    # An iterator is consumed once — the second pass sees nothing.
    it = enumerate(xs)
    print(f"first pass: {list(it)}")
    print(f"second pass: {list(it)}  (exhausted)")


if __name__ == "__main__":
    main()
