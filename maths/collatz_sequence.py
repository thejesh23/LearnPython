"""The Collatz sequence, and finding the longest chain below a bound.

The rule could not be simpler: if n is even, halve it; if n is odd, replace it
with 3n + 1. Repeat. Every starting value tested so far eventually reaches 1,
but nobody has proved that it always does. That open question is the Collatz
conjecture, and it is why this file computes rather than proves anything.

Chain lengths behave erratically: 27 takes 111 steps to reach 1 and climbs as
high as 9232 on the way, while its neighbours finish in a couple of dozen.
That irregularity is what makes memoisation pay. A naive scan of every start
below n recomputes the same tails over and over; caching the length of each
value seen means each number is expanded at most once, and most chains hit a
cached value within a few steps.

Cost without a cache is roughly O(n * average chain length); with one it is
close to O(n), at the price of holding a dictionary of results.
"""


def collatz_sequence(n: int) -> list[int]:
    """The full path from n down to 1, inclusive at both ends."""
    if n < 1:
        raise ValueError("the Collatz map is defined for n >= 1")
    path = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        path.append(n)
    return path


def collatz_length(n: int) -> int:
    """Number of values in the chain from n to 1, so length(1) == 1."""
    if n < 1:
        raise ValueError("the Collatz map is defined for n >= 1")
    count = 1
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        count += 1
    return count


def collatz_length_cached(n: int, cache: dict[int, int]) -> int:
    """Chain length using and filling a shared cache, without recursion."""
    if n < 1:
        raise ValueError("the Collatz map is defined for n >= 1")
    # Walk forward collecting unknown values, then fill them in on the way back.
    stack: list[int] = []
    while n not in cache:
        stack.append(n)
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    length = cache[n]
    while stack:
        length += 1
        cache[stack.pop()] = length
    return length


def longest_chain_below(limit: int) -> tuple[int, int]:
    """The start below limit with the longest chain, and that chain's length."""
    cache: dict[int, int] = {1: 1}
    best_start, best_length = 1, 1
    for start in range(1, limit):
        length = collatz_length_cached(start, cache)
        if length > best_length:
            best_start, best_length = start, length
    return best_start, best_length


def main() -> None:
    print(f"sequence from 6:  {collatz_sequence(6)}")
    print(f"sequence from 7:  {collatz_sequence(7)}")
    print(f"sequence from 1:  {collatz_sequence(1)}")

    print(f"length(27) = {collatz_length(27)}")
    print(f"peak of 27 = {max(collatz_sequence(27))}")

    cache: dict[int, int] = {1: 1}
    same = all(collatz_length(n) == collatz_length_cached(n, cache)
               for n in range(1, 2000))
    print(f"cached and plain agree for 1..1999: {same}")

    for limit in (10, 1000, 100_000, 1_000_000):
        start, length = longest_chain_below(limit)
        print(f"longest chain below {limit:>9}: start {start:>7}, "
              f"{length} terms")

    try:
        collatz_length(0)
    except ValueError as exc:
        print(f"rejected 0: {exc}")


if __name__ == "__main__":
    main()
