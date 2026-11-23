"""Arithmetic modulo m: inverses, the Chinese remainder theorem, square roots and logs."""

import math


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return (g, x, y) with a*x + b*y == g == gcd(a, b)."""
    old_r, r, old_x, x, old_y, y = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y
    return old_r, old_x, old_y


def mod_inverse(a: int, m: int) -> int:
    """The x in [0, m) with a*x == 1 (mod m); ValueError if gcd(a, m) != 1."""
    if m < 1:
        raise ValueError("modulus must be positive")
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"{a} has no inverse modulo {m}")
    return x % m


def crt(remainders: list[int], moduli: list[int]) -> tuple[int, int]:
    """Smallest x >= 0 with x == r_i (mod m_i) for all i, and the combined modulus.

    Moduli may share factors: congruences are merged two at a time, and a
    ValueError means they contradict each other.
    """
    if len(remainders) != len(moduli):
        raise ValueError("need one remainder per modulus")
    x, m = 0, 1  # the empty system: everything mod 1
    for r2, m2 in zip(remainders, moduli):
        if m2 < 1:
            raise ValueError("moduli must be positive")
        g, p, _ = extended_gcd(m, m2)
        if (r2 - x) % g:
            raise ValueError("the congruences contradict each other")
        lcm = m // g * m2
        x = (x + m * ((r2 - x) // g * p % (m2 // g))) % lcm
        m = lcm
    return x, m


def legendre(a: int, p: int) -> int:
    """Euler's criterion: 1 if a is a nonzero square mod odd prime p, -1 if not, 0 if p | a."""
    r = pow(a, (p - 1) // 2, p)
    return -1 if r == p - 1 else r


def sqrt_mod(a: int, p: int) -> int | None:
    """Tonelli-Shanks: some x with x*x == a (mod odd prime p), or None if there is none."""
    a %= p
    if a == 0:
        return 0
    if legendre(a, p) != 1:
        return None
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    q, s = p - 1, 0
    while q % 2 == 0:
        q, s = q // 2, s + 1
    z = next(z for z in range(2, p) if legendre(z, p) == -1)
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:  # least i with t^(2^i) == 1
            t2, i = t2 * t2 % p, i + 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
    return r


def discrete_log(g: int, h: int, p: int) -> int | None:
    """Baby-step giant-step: least x >= 0 with g^x == h (mod p), in O(sqrt p) steps.

    Works for any modulus p > 1 as long as g is coprime to it.
    """
    if p < 2 or math.gcd(g, p) != 1:
        raise ValueError("need p > 1 and g coprime to p")
    g, h = g % p, h % p
    n = math.isqrt(p) + 1
    baby: dict[int, int] = {}
    value = 1
    for j in range(n):  # baby steps: g^j for j < n
        baby.setdefault(value, j)
        value = value * g % p
    giant = pow(g, -n, p)  # stepping back by n each time
    gamma = h
    for i in range(n + 1):  # giant steps: h * g^(-i*n), looking for a baby step
        if gamma in baby:
            return i * n + baby[gamma]
        gamma = gamma * giant % p
    return None
