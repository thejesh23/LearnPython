"""Pollard's rho: find a factor of a composite in roughly O(n**0.25) steps.

Trial division needs sqrt(n) work. Pollard's rho gets to the fourth root by
gambling on the birthday paradox. Iterate a pseudo-random map, here
f(x) = x*x + c mod n. If p is an unknown prime factor of n, the same sequence
viewed modulo p is also pseudo-random but lives in a set of only p elements,
so it repeats after about sqrt(p) steps. When two values collide modulo p but
not modulo n, their difference is a multiple of p and gcd(difference, n) hands
you a real factor.

You cannot see the sequence modulo p, so instead you detect the cycle in the
full sequence and test gcds as you go. Brent's variant is the efficient way:
it compares against a checkpoint whose distance doubles, which needs one
evaluation of f per step instead of Floyd's three, and it batches many
differences into a single product so one gcd covers a whole block.

Two ways the attempt can fail. A gcd of n means the batch swallowed every
factor, so back up and test the differences one at a time. A gcd stuck at 1
means this c was unlucky, so retry with a different one. Neither loses
correctness, only time.

Combined with Miller-Rabin to decide when to stop recursing, this factors
64-bit numbers essentially instantly.
"""

import math
import random

WITNESSES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def is_prime(n: int) -> bool:
    """Deterministic Miller-Rabin for anything a 64-bit integer can hold."""
    if n < 2:
        return False
    for p in WITNESSES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in WITNESSES:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def pollard_rho(n: int) -> int:
    """A nontrivial factor of composite n, using Brent's cycle detection."""
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    while True:
        y = random.randrange(1, n)
        c = random.randrange(1, n)
        m = 128  # how many differences to batch into one gcd
        g = q = r = 1
        x = ys = y
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n  # accumulate, gcd once per batch
                g = math.gcd(q, n)
                k += m
            r *= 2  # Brent doubles the checkpoint distance
        if g == n:
            # The batch hid the factor: replay the last block one step at a
            # time to find where the gcd first became nontrivial.
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = math.gcd(abs(x - ys), n)
        if g != n:
            return g
        # g == n even after the replay: this c was unlucky, so pick another.


def factorise(n: int) -> list[int]:
    """All prime factors of n with multiplicity, in ascending order."""
    if n < 1:
        raise ValueError("factorisation is defined for n >= 1")
    if n == 1:
        return []
    factors: list[int] = []
    stack = [n]
    while stack:
        value = stack.pop()
        if value == 1:
            continue
        if is_prime(value):
            factors.append(value)
            continue
        divisor = pollard_rho(value)
        stack.append(divisor)
        stack.append(value // divisor)
    return sorted(factors)


def divisors(n: int) -> list[int]:
    """Every divisor of n, built up from the prime factorisation."""
    result = [1]
    for p in factorise(n):
        result += [d * p for d in result]
    return sorted(set(result))


def main() -> None:
    random.seed(0)  # deterministic output for a teaching example

    for n in (1, 2, 12, 97, 1024, 600_851_475_143):
        print(f"factorise({n}) = {factorise(n)}")

    # A semiprime of two 10-digit primes: hopeless for trial division.
    semiprime = 1_000_000_007 * 1_000_000_009
    print(f"factorise({semiprime}) = {factorise(semiprime)}")

    # A square of a prime, where the two factors are equal.
    print(f"factorise(1000003**2) = {factorise(1000003**2)}")

    # Close to the 64-bit ceiling.
    big = 2**64 - 1
    print(f"factorise(2**64 - 1) = {factorise(big)}")

    print(f"divisors(60) = {divisors(60)}")

    ok = all(math.prod(factorise(n)) == n for n in range(1, 500))
    print(f"factors multiply back to n for 1..499: {ok}")
    all_prime = all(is_prime(p) for n in range(2, 500) for p in factorise(n))
    print(f"every reported factor is prime: {all_prime}")


if __name__ == "__main__":
    main()
