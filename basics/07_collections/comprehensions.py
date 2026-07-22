"""Comprehensions — build a collection from an iterable in one expression.

    [expr for item in iterable if condition]

They exist for list, set, and dict. Wrapping the same thing in parentheses
gives a *generator expression*, which produces values lazily instead of
building the whole result in memory.

The rule of thumb: a comprehension should read like the sentence it replaces.
Two loops and a condition is usually the point to go back to a plain `for`.
"""


def main() -> None:
    nums = range(1, 11)

    print(f"squares      = {[n * n for n in nums]}")
    print(f"even squares = {[n * n for n in nums if n % 2 == 0]}")

    # The conditional expression form transforms rather than filters.
    print(f"clamped      = {[n if n < 5 else 5 for n in nums]}")

    # Set and dict comprehensions.
    words = ["apple", "avocado", "banana"]
    print(f"initials (set)  = {{'a', 'b'}} -> {  {w[0] for w in words} }")
    print(f"lengths (dict)  = { {w: len(w) for w in words} }")

    # Nested loops: the order reads exactly like the nested for statements.
    pairs = [(x, y) for x in range(3) for y in range(2)]
    print(f"pairs = {pairs}")

    # Flattening a nested list.
    grid = [[1, 2], [3, 4], [5]]
    print(f"flattened = {[cell for row in grid for cell in row]}")

    # Generator expression: lazy, no intermediate list.
    total = sum(n * n for n in range(1_000_000))
    print(f"sum of squares below 1e6 = {total}  (no list was built)")

    gen = (n * n for n in range(5))
    print(f"generator object: {gen}")
    print(f"consumed once: {list(gen)}, then empty: {list(gen)}")

    # any/all take generator expressions and short-circuit.
    print(f"any even?  {any(n % 2 == 0 for n in nums)}")
    print(f"all positive? {all(n > 0 for n in nums)}")

    # A comprehension has its own scope: the loop name does not leak.
    n = "untouched"
    _ = [n for n in range(3)]
    print(f"n after the comprehension = {n!r}")


if __name__ == "__main__":
    main()
