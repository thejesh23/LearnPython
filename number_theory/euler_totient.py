"""Euler's totient phi(n): how many of 1..n are coprime to n.

Counting one by one is O(n log n) and misses the structure. The useful fact is
that phi is multiplicative across coprime parts, and for a prime power the
count is easy: among 1..p**k exactly the multiples of p are excluded, so
phi(p**k) = p**k - p**(k-1). Putting those together gives the product formula
phi(n) = n * prod over distinct primes p dividing n of (1 - 1/p).

That turns a single evaluation into a factorisation, which trial division does
in O(sqrt(n)). Written with integer arithmetic as result -= result // p it
stays exact, no floating point involved.

When you need phi for every n up to a bound, factorising each one is wasteful.
A sieve does better: start each slot at n, then for each prime p sweep its
multiples applying the (1 - 1/p) factor once. Every value is touched once per
distinct prime factor, so the whole table costs O(N log log N).

phi is what makes Euler's theorem work: a**phi(n) == 1 (mod n) whenever a and
n are coprime, which generalises Fermat's little theorem and underpins RSA.
"""

import math


def totient(n: int) -> int:
    """phi(n) by trial-dividing out each distinct prime factor."""
    if n < 1:
        raise ValueError("phi is defined for n >= 1")
    result = n
    p = 2
    remaining = n
    while p * p <= remaining:
        if remaining % p == 0:
            while remaining % p == 0:
                remaining //= p  # strip the whole prime power in one go
            result -= result // p  # exact integer form of result * (1 - 1/p)
        p += 1 if p == 2 else 2
    if remaining > 1:
        result -= result // remaining  # one large prime factor is left
    return result


def totient_bruteforce(n: int) -> int:
    """The definition itself, used to check the fast version."""
    return sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)


def totient_sieve(limit: int) -> list[int]:
    """phi(0..limit) in one pass, phi[0] left as 0."""
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:  # untouched, so p is prime
            for multiple in range(p, limit + 1, p):
                phi[multiple] -= phi[multiple] // p
    return phi


def main() -> None:
    for n in (1, 2, 9, 10, 12, 36, 97, 1_000_000):
        print(f"phi({n}) = {totient(n)}")

    table = totient_sieve(20)
    print(f"phi(0..20) = {table}")

    fast_ok = all(totient(n) == totient_bruteforce(n) for n in range(1, 500))
    print(f"formula matches the definition for 1..499: {fast_ok}")
    sieve_ok = totient_sieve(500)[1:] == [totient(n) for n in range(1, 501)]
    print(f"sieve matches the formula for 1..500: {sieve_ok}")

    # For prime p, phi(p) == p - 1, so every nonzero residue is invertible.
    print(f"phi(13) = {totient(13)} (13 is prime)")
    print(f"phi(2**10) = {totient(2**10)} (half of 1024)")

    # Euler's theorem in action, for a modulus that is not prime.
    n, a = 100, 3
    print(f"phi(100) = {totient(100)}, "
          f"3**phi(100) mod 100 = {pow(a, totient(n), n)}")

    try:
        totient(0)
    except ValueError as exc:
        print(f"rejected 0: {exc}")


if __name__ == "__main__":
    main()
