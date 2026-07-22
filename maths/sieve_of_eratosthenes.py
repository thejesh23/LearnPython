"""Sieve of Eratosthenes: find every prime below n by crossing out multiples.

Instead of asking "is this one number prime?" the sieve answers the question
for a whole range at once. Walk upwards; the first number not yet crossed out
must be prime, because nothing below it divides it. Then cross out all of its
multiples, since they are visibly composite.

Two details make it efficient. Crossing out can start at p * p rather than
2 * p, because every smaller multiple of p has a factor below p and was struck
already. And the outer loop only needs to reach sqrt(n), for the same reason.
The total work is the sum of n/p over primes p below sqrt(n), which is
O(n log log n) — very close to linear.

Space is the real cost: one flag per number. A bytearray keeps that to one
byte each and lets slice assignment do the striking in C. For ranges too big
to hold at once, a segmented sieve sieves [lo, hi) using only the primes below
sqrt(hi), so memory depends on the window size, not on hi.
"""


def sieve(limit: int) -> list[int]:
    """Every prime strictly below limit."""
    if limit < 3:
        return []
    flags = bytearray([1]) * limit
    flags[0] = flags[1] = 0
    p = 2
    while p * p < limit:
        if flags[p]:
            # Slice assignment strikes the whole arithmetic progression at once.
            start = p * p
            flags[start::p] = bytearray(len(range(start, limit, p)))
        p += 1
    return [i for i in range(limit) if flags[i]]


def prime_count(limit: int) -> int:
    """Count primes below limit without materialising the list."""
    if limit < 3:
        return 0
    flags = bytearray([1]) * limit
    flags[0] = flags[1] = 0
    p = 2
    while p * p < limit:
        if flags[p]:
            start = p * p
            flags[start::p] = bytearray(len(range(start, limit, p)))
        p += 1
    return sum(flags)


def segmented_sieve(lo: int, hi: int) -> list[int]:
    """Primes in [lo, hi) using memory proportional to the window, not to hi."""
    if hi <= 2 or hi <= lo:
        return []
    lo = max(lo, 2)
    base = sieve(int(hi**0.5) + 1)
    flags = bytearray([1]) * (hi - lo)
    for p in base:
        # First multiple of p that is >= lo, but never p itself.
        start = max(p * p, ((lo + p - 1) // p) * p)
        for m in range(start, hi, p):
            flags[m - lo] = 0
    return [lo + i for i, ok in enumerate(flags) if ok]


def main() -> None:
    print(f"primes below 50: {sieve(50)}")
    print(f"primes below 2:  {sieve(2)}")
    print(f"primes below 3:  {sieve(3)}")

    print(f"count below 100:       {prime_count(100)}")
    print(f"count below 1_000_000: {prime_count(1_000_000)}")

    window = segmented_sieve(1_000_000, 1_000_100)
    print(f"primes in [1e6, 1e6+100): {window}")

    # The segmented sieve must agree with the plain one on a shared range.
    print(f"segments agree: {segmented_sieve(0, 50) == sieve(50)}")


if __name__ == "__main__":
    main()
