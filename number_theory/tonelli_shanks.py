"""Tonelli-Shanks: modular square roots — solving x^2 = n (mod p) for prime p.

Ordinary square roots do not exist mod p for every n; exactly half the non-zero
residues are quadratic residues (have a root), told apart by Euler's criterion
n^((p-1)/2) mod p, which is +1 for residues and -1 for non-residues.

When p = 3 (mod 4) a root is simply n^((p+1)/4). The general case is
Tonelli-Shanks: write p-1 = q * 2^s with q odd, and iteratively correct a
candidate root using a fixed non-residue, halving the order of an error term
each round until it vanishes. It runs in O(log^2 p) multiplications.

Modular roots underpin point decompression on elliptic curves and several
factoring and primality routines.
"""


def legendre(n: int, p: int) -> int:
    """+1 if n is a non-zero quadratic residue mod p, -1 if not, 0 if divisible."""
    result = pow(n % p, (p - 1) // 2, p)
    return result - p if result > 1 else result


def tonelli_shanks(n: int, p: int) -> int | None:
    """A square root of n mod p, or None if none exists. p must be an odd prime."""
    n %= p
    if n == 0:
        return 0
    if legendre(n, p) != 1:
        return None  # n is a non-residue
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)  # the easy case

    # Factor p - 1 = q * 2^s with q odd.
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1

    # Find any quadratic non-residue z.
    z = 2
    while legendre(z, p) != -1:
        z += 1

    m, c, t, r = s, pow(z, q, p), pow(n, q, p), pow(n, (q + 1) // 2, p)
    while t != 1:
        # Find the least i with t^(2^i) == 1.
        i, temp = 0, t
        while temp != 1:
            temp = temp * temp % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)  # correction factor
        m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
    return r


def main() -> None:
    print("Euler's criterion splits residues from non-residues (mod 13):")
    residues = [n for n in range(1, 13) if legendre(n, 13) == 1]
    print(f"  quadratic residues mod 13: {residues}")
    print(f"  exactly (p-1)/2 = 6 of them: {len(residues) == 6}")

    cases = [(10, 13), (5, 41), (2, 113), (n := 1234, p := 5915587277)]
    for n, p in cases:
        root = tonelli_shanks(n, p)
        if root is None:
            print(f"  x^2 = {n} (mod {p}): no solution")
        else:
            check = root * root % p
            print(f"  x^2 = {n} (mod {p}): x = {root}, and x^2 mod p = {check} "
                  f"(both roots: {root}, {p - root})")

    print("non-residues correctly report no root:")
    print(f"  x^2 = 5 (mod 7) -> {tonelli_shanks(5, 7)}  (5 is a non-residue mod 7)")

    # Exhaustive check: every residue mod a prime is recovered.
    p = 97
    ok = True
    for x in range(1, p):
        n = x * x % p
        root = tonelli_shanks(n, p)
        if root is None or root * root % p != n:
            ok = False
    print(f"every residue mod {p} has a verified root: {ok}")


if __name__ == "__main__":
    main()
