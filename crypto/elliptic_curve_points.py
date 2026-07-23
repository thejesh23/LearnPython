"""Elliptic curve point arithmetic over a prime field — the ECC foundation.

An elliptic curve is the set of points (x, y) satisfying y^2 = x^3 + ax + b
(mod p), plus a "point at infinity" that acts as the identity. Those points
form a group under a geometric addition rule: to add P and Q, draw the line
through them, find the third intersection with the curve, and reflect it over
the x-axis. Doubling uses the tangent line instead.

The security of ECC comes from the same discrete-log hardness as Diffie-Hellman
but in this group, where the best known attacks are far slower per bit — which
is why a 256-bit curve matches the strength of a 3072-bit RSA key.

This implements the group law and scalar multiplication (double-and-add). It is
for understanding only; real ECC needs constant-time code to resist timing
attacks. This uses the standard secp256k1 parameters.
"""

# secp256k1: y^2 = x^3 + 7 over F_p
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
A, B = 0, 7
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141  # group order

Point = tuple[int, int] | None  # None is the point at infinity (identity)


def is_on_curve(point: Point) -> bool:
    if point is None:
        return True
    x, y = point
    return (y * y - (x * x * x + A * x + B)) % P == 0


def add(p_pt: Point, q_pt: Point) -> Point:
    if p_pt is None:
        return q_pt
    if q_pt is None:
        return p_pt
    x1, y1 = p_pt
    x2, y2 = q_pt
    if x1 == x2 and (y1 + y2) % P == 0:
        return None  # P + (-P) = identity
    if p_pt == q_pt:
        # Tangent slope: (3x^2 + a) / (2y).
        slope = (3 * x1 * x1 + A) * pow(2 * y1, -1, P) % P
    else:
        slope = (y2 - y1) * pow(x2 - x1, -1, P) % P
    x3 = (slope * slope - x1 - x2) % P
    y3 = (slope * (x1 - x3) - y1) % P
    return x3, y3


def scalar_mult(k: int, point: Point) -> Point:
    """k * point by double-and-add: O(log k) additions."""
    result: Point = None
    addend = point
    k %= N
    while k:
        if k & 1:
            result = add(result, addend)
        addend = add(addend, addend)  # double
        k >>= 1
    return result


def main() -> None:
    G = (GX, GY)
    print(f"generator on curve: {is_on_curve(G)}")

    # The group law: 2G, 3G, and associativity.
    g2 = scalar_mult(2, G)
    g3 = scalar_mult(3, G)
    print(f"2G on curve: {is_on_curve(g2)}, 3G on curve: {is_on_curve(g3)}")
    print(f"G + 2G == 3G: {add(G, g2) == g3}")
    print(f"addition commutes: {add(G, g2) == add(g2, G)}")

    # Identity and inverse.
    print(f"G + O == G: {add(G, None) == G}")
    neg_g = (GX, (-GY) % P)
    print(f"G + (-G) == O: {add(G, neg_g) is None}")

    # n * G = identity, since n is the group order.
    print(f"N * G is the point at infinity: {scalar_mult(N, G) is None}")

    # ECDH: two parties reach the same shared point.
    import secrets

    a = secrets.randbelow(N - 1) + 1
    b = secrets.randbelow(N - 1) + 1
    alice_pub = scalar_mult(a, G)
    bob_pub = scalar_mult(b, G)
    shared_a = scalar_mult(a, bob_pub)
    shared_b = scalar_mult(b, alice_pub)
    print(f"ECDH shared point matches: {shared_a == shared_b}")
    print(f"  x-coordinate: {hex(shared_a[0])[:22]}...")

    # Scalar multiplication distributes: (j + k)G = jG + kG.
    j, k = 12345, 67890
    print(f"(j+k)G == jG + kG: "
          f"{scalar_mult(j + k, G) == add(scalar_mult(j, G), scalar_mult(k, G))}")
    print("the discrete log — recovering k from kG — is what keeps the key secret")


if __name__ == "__main__":
    main()
