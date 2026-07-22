"""Project Euler 14: the longest Collatz chain starting under one million.

The naive search recomputes the tail of nearly every chain — the sequence from
27 alone passes through 111 numbers that other starts will visit again.
Memoising chain lengths turns the whole search from tens of millions of steps
into roughly one step per distinct value ever seen.

The recursion is deep enough to blow Python's stack, so the iterative version
below collects the unmemoised prefix into a list and then fills the cache
backwards.

Answer: 837799, with a chain of 525 terms.
"""


def chain_length(n: int, cache: dict[int, int]) -> int:
    """Iterative, so a long chain cannot overflow the interpreter stack."""
    path: list[int] = []
    current = n
    while current not in cache:
        path.append(current)
        current = current // 2 if current % 2 == 0 else 3 * current + 1
    length = cache[current]
    for value in reversed(path):  # fill in the prefix, longest last
        length += 1
        cache[value] = length
    return cache[n]


def longest_chain_under(limit: int) -> tuple[int, int]:
    cache: dict[int, int] = {1: 1}
    best_start, best_length = 1, 1
    for n in range(2, limit):
        length = chain_length(n, cache)
        if length > best_length:
            best_start, best_length = n, length
    return best_start, best_length


def sequence(n: int) -> list[int]:
    out = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        out.append(n)
    return out


def main() -> None:
    print(f"sequence from 13: {sequence(13)}")
    print(f"length: {len(sequence(13))}")

    start, length = longest_chain_under(1_000_000)
    print(f"longest chain below 1,000,000: starts at {start}, {length} terms")
    print(f"verified by direct generation: {len(sequence(start)) == length}")

    cache: dict[int, int] = {1: 1}
    longest_chain_under(1_000_000)
    print(f"27 takes {len(sequence(27))} steps — famously long for its size")

    for bound in (10, 100, 1000):
        print(f"  below {bound:>5}: {longest_chain_under(bound)}")


if __name__ == "__main__":
    main()
