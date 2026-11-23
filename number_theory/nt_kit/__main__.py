"""Examples and self-check: python3 -m number_theory.nt_kit"""

import math
import random
import sys

from . import (
    crt,
    discrete_log,
    divisors,
    extended_gcd,
    factorize,
    is_prime,
    mod_inverse,
    next_prime,
    sqrt_mod,
    totient,
)


def examples() -> None:
    g, x, y = extended_gcd(240, 46)
    print(f"1. extended gcd: 240*{x} + 46*{y} = {g} | inverse of 3 mod 11 = {mod_inverse(3, 11)}")
    print("2. CRT x=2 (3), 3 (5), 2 (7):", crt([2, 3, 2], [3, 5, 7]),
          "| x=3 (6), 7 (10):", crt([3, 7], [6, 10]))
    p = next_prime(10**12)
    print(f"3. next prime after 10^12: {p} | 2^61-1 prime: {is_prime(2**61 - 1)} "
          f"| 561 (Carmichael) prime: {is_prime(561)}")
    print("4. factorize 600851475143:", factorize(600851475143),
          "| 1000003 * 1000033:", factorize(1000003 * 1000033))
    print("5. divisors of 360:", len(divisors(360)), divisors(360)[:8], "... | phi(360) =", totient(360))
    print("6. sqrt of 10 mod 13:", sqrt_mod(10, 13), "| of 5 mod 13:", sqrt_mod(5, 13),
          "| of 2 mod 10^9+9:", sqrt_mod(2, 10**9 + 9))
    x = discrete_log(5, 8, 1_000_003)
    print(f"7. discrete log: 5^x = 8 (mod 1000003) at x = {x}; check {pow(5, x, 1_000_003)}")


def brute_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def self_check() -> None:
    rng = random.Random(17)
    assert [n for n in range(3000) if is_prime(n)] == [n for n in range(3000) if brute_prime(n)]
    for n in [1, 2, 3, 4, 49, 121, 2**20] + [rng.randrange(2, 10**15) for _ in range(150)]:
        f = factorize(n, rng)
        assert math.prod(f) == n and all(is_prime(p) for p in f), (n, f)
    for _ in range(20):
        a, b = next_prime(rng.randrange(10**9)), next_prime(rng.randrange(10**9))
        assert factorize(a * b, rng) == sorted([a, b])
    for n in range(1, 400):
        assert divisors(n) == [d for d in range(1, n + 1) if n % d == 0]
        assert totient(n) == sum(math.gcd(k, n) == 1 for k in range(1, n + 1))
    for _ in range(300):
        a, b = rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6)
        g, x, y = extended_gcd(a, b)
        assert a * x + b * y == g and abs(g) == math.gcd(a, b)
        m = rng.randint(2, 10**6)
        if math.gcd(a, m) == 1:
            assert mod_inverse(a, m) == pow(a, -1, m)
    for _ in range(200):
        moduli = [rng.randint(1, 12) for _ in range(rng.randint(1, 3))]
        rems = [rng.randrange(m) for m in moduli]
        hits = [x for x in range(math.lcm(*moduli)) if all(x % m == r for r, m in zip(rems, moduli))]
        try:
            assert crt(rems, moduli) == (hits[0], math.lcm(*moduli))
        except ValueError:
            assert not hits
    for p in [q for q in range(3, 400) if brute_prime(q)]:
        squares = {x * x % p for x in range(p)}
        for a in range(p):
            r = sqrt_mod(a, p)
            assert (r is None) == (a not in squares) and (r is None or r * r % p == a)
        g, h = rng.randrange(1, p), rng.randrange(1, p)
        powers = [pow(g, x, p) for x in range(p)]
        assert discrete_log(g, h, p) == (powers.index(h) if h in powers else None)
    for bad in (lambda: mod_inverse(6, 9), lambda: crt([1, 2], [4, 6]), lambda: factorize(0)):
        try:
            bad()
        except ValueError:
            pass
        else:
            raise AssertionError("bad input accepted")


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
