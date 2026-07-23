"""Shamir's secret sharing: split a secret so any k of n shares reconstruct it.

A polynomial of degree k-1 is fixed by exactly k points. Put the secret as the
constant term, pick the other k-1 coefficients at random, and hand each party
one point on the curve. Any k points recover the whole polynomial by Lagrange
interpolation, and evaluating it at x=0 gives back the secret. Fewer than k
points leave the constant term perfectly undetermined — every value is equally
likely — so the scheme is information-theoretically secure, not merely hard to
break.

All arithmetic is done in a finite field modulo a prime larger than the secret,
so the shares leak nothing through their size and the interpolation is exact.

Splitting is O(n*k); reconstruction from k shares is O(k^2).
"""

import secrets

PRIME = 2**521 - 1  # a Mersenne prime, comfortably larger than any secret here


def split_secret(secret: int, n: int, k: int, prime: int = PRIME) -> list[tuple[int, int]]:
    if secret >= prime:
        raise ValueError("secret must be smaller than the field prime")
    # coeffs[0] is the secret; the rest are random.
    coeffs = [secret] + [secrets.randbelow(prime) for _ in range(k - 1)]
    shares = []
    for x in range(1, n + 1):  # x = 0 would hand out the secret directly
        y = 0
        for coeff in reversed(coeffs):  # Horner evaluation
            y = (y * x + coeff) % prime
        shares.append((x, y))
    return shares


def reconstruct(shares: list[tuple[int, int]], prime: int = PRIME) -> int:
    """Lagrange interpolation evaluated at x = 0."""
    secret = 0
    for i, (xi, yi) in enumerate(shares):
        numerator = denominator = 1
        for j, (xj, _) in enumerate(shares):
            if i == j:
                continue
            numerator = numerator * (-xj) % prime
            denominator = denominator * (xi - xj) % prime
        lagrange = yi * numerator % prime * pow(denominator, -1, prime) % prime
        secret = (secret + lagrange) % prime
    return secret


def main() -> None:
    secret = int.from_bytes(b"launch code: 4815", "big")
    print(f"secret (as int): {secret}")

    shares = split_secret(secret, n=5, k=3)
    print("5 shares issued, any 3 reconstruct:")
    for x, y in shares:
        print(f"  share {x}: {str(y)[:24]}...")

    # Any quorum of 3 works.
    for chosen in ([shares[0], shares[2], shares[4]], shares[:3], shares[-3:]):
        got = reconstruct(chosen)
        xs = [s[0] for s in chosen]
        print(f"  shares {xs} -> {'recovered' if got == secret else 'WRONG'}")

    recovered = reconstruct(shares[:3])
    print(f"recovered bytes: {recovered.to_bytes((recovered.bit_length() + 7) // 8, 'big')!r}")

    # Fewer than k shares reveal nothing — a wrong 2-share "reconstruction"
    # lands on an unrelated value.
    two = reconstruct(shares[:2])
    print(f"only 2 shares -> {str(two)[:24]}... (not the secret: {two != secret})")

    # A tiny field makes the point-counting concrete.
    small = 1234
    toy_shares = split_secret(small, n=4, k=2, prime=7919)
    print(f"toy field: secret {small}, 2 of {len(toy_shares)} shares -> "
          f"{reconstruct(toy_shares[:2], prime=7919)}")
    print("k-1 shares leave the constant term uniformly distributed — perfect secrecy")


if __name__ == "__main__":
    main()
