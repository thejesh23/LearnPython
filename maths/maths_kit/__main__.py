"""Examples and self-check: python3 -m maths.maths_kit"""

import math
import random
import sys

from . import (
    comb,
    from_base,
    gcd,
    is_prime,
    isqrt,
    lcm,
    power_mod,
    prime_factors,
    primes_below,
    to_base,
)


def examples() -> None:
    print("1. gcd(84, 36, 120) =", gcd(84, 36, 120), "| lcm(4, 6, 10) =", lcm(4, 6, 10))
    print("2. 3 ** (2 ** 1000) mod 1e9+7 =", power_mod(3, 2**1000, 1_000_000_007),
          "(the full power has over 10**300 digits)")
    big = (2**60 + 1) ** 2
    print("3. isqrt of a 121-bit square:", isqrt(big) == 2**60 + 1,
          "| float sqrt gets it right:", int(big**0.5) == 2**60 + 1)
    print("4. poker hands C(52, 5) =", comb(52, 5), "| Pascal row 6:", [comb(6, r) for r in range(7)])
    print("5. 2024 in base 2, 16, 36:", to_base(2024, 2), to_base(2024, 16), to_base(2024, 36),
          "| 'zz' base 36 =", from_base("zz", 36))
    print("6. primes below 50:", primes_below(50))
    print("7. is 561 prime?", is_prime(561), "->", prime_factors(561),
          "| 1_000_000_007:", is_prime(1_000_000_007))


def self_check() -> None:
    rng = random.Random(42)
    sieve = set(primes_below(5000))
    assert all(is_prime(n) == (n in sieve) for n in range(-5, 5000))
    assert len(primes_below(10**5)) == 9592  # known value of pi(10**5)
    for _ in range(500):
        a, b = rng.randint(-10**12, 10**12), rng.randint(-10**6, 10**6)
        assert gcd(a, b) == math.gcd(a, b) and lcm(a, b) == math.lcm(a, b)
        n = rng.randint(0, 10**40)
        assert isqrt(n) == math.isqrt(n)
        base, exp, mod = rng.randint(-10**6, 10**6), rng.randint(0, 10**6), rng.randint(1, 10**9)
        assert power_mod(base, exp, mod) == pow(base, exp, mod)
        r_n = rng.randint(0, 200)
        r = rng.randint(-2, r_n + 2)
        assert comb(r_n, r) == (math.comb(r_n, r) if r >= 0 else 0)
        k = rng.randint(2, 36)
        assert from_base(to_base(a, k), k) == a == int(to_base(a, k), k)
        m = rng.randint(1, 10**7)
        factors = prime_factors(m)
        assert math.prod(p**e for p, e in factors.items()) == m and all(map(is_prime, factors))
    assert gcd() == 0 and lcm() == 1 and to_base(0, 2) == "0" and prime_factors(1) == {}
    try:
        from_base("129", 8)
    except ValueError:
        pass
    else:
        raise AssertionError("'9' accepted as an octal digit")


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
