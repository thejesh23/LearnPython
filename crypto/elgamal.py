"""ElGamal encryption — public-key encryption built on Diffie-Hellman.

Where RSA hides a message behind factoring, ElGamal hides it behind the
discrete logarithm. The public key is y = g^x mod p for a secret x. To encrypt
m, the sender picks a fresh random k and sends the pair (g^k, m * y^k). The
receiver computes (g^k)^x = y^k and divides it out to recover m.

Two properties fall out of the construction. It is randomised — the same
plaintext encrypts differently every time, because of k — which fixes the
determinism that plagues textbook RSA. And it is homomorphic under
multiplication: the product of two ciphertexts decrypts to the product of the
plaintexts, which is the seed of more advanced protocols.

The one non-negotiable rule: k must be fresh and random per message. Reusing k
across two messages leaks their ratio. Illustrative only; use a vetted library.
"""

import secrets


def generate_keys(p: int, g: int) -> tuple[int, int]:
    """Return (private x, public y = g^x mod p)."""
    x = secrets.randbelow(p - 2) + 1
    y = pow(g, x, p)
    return x, y


def encrypt(m: int, p: int, g: int, y: int) -> tuple[int, int]:
    k = secrets.randbelow(p - 2) + 1  # ephemeral, MUST be fresh each time
    c1 = pow(g, k, p)
    c2 = m * pow(y, k, p) % p
    return c1, c2


def decrypt(cipher: tuple[int, int], x: int, p: int) -> int:
    c1, c2 = cipher
    shared = pow(c1, x, p)  # = y^k
    return c2 * pow(shared, -1, p) % p


def main() -> None:
    # A safe prime and generator (small, for a readable demo).
    p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A63A3620FFFFFFFFFFFFFFFF
    g = 2
    x, y = generate_keys(p, g)
    print(f"{p.bit_length()}-bit prime, public key generated")

    m = int.from_bytes(b"attack at dawn", "big")
    cipher = encrypt(m, p, g, y)
    print(f"encrypt -> (c1, c2), each ~{cipher[0].bit_length()} bits")
    print(f"round-trip: {decrypt(cipher, x, p) == m}")

    # Randomised: same message, different ciphertext each time.
    c_a = encrypt(m, p, g, y)
    c_b = encrypt(m, p, g, y)
    print(f"non-deterministic (fresh k): {c_a != c_b}, both decrypt to m: "
          f"{decrypt(c_a, x, p) == m == decrypt(c_b, x, p)}")

    # Multiplicatively homomorphic: E(m1) * E(m2) decrypts to m1 * m2.
    m1, m2 = 6, 7
    e1 = encrypt(m1, p, g, y)
    e2 = encrypt(m2, p, g, y)
    product = (e1[0] * e2[0] % p, e1[1] * e2[1] % p)
    print(f"homomorphic: E(6)*E(7) decrypts to {decrypt(product, x, p)} (= 42)")

    # The k-reuse danger, on a small field for clarity.
    print("k reuse leaks the ratio of two messages:")
    small_p, small_g = 2087, 5
    sx, sy = generate_keys(small_p, small_g)
    k = secrets.randbelow(small_p - 2) + 1  # deliberately reused
    ca = (pow(small_g, k, small_p), 100 * pow(sy, k, small_p) % small_p)
    cb = (pow(small_g, k, small_p), 133 * pow(sy, k, small_p) % small_p)
    # Same c1 -> same y^k -> c2a / c2b = m_a / m_b, no private key needed.
    ratio = ca[1] * pow(cb[1], -1, small_p) % small_p
    expected = 100 * pow(133, -1, small_p) % small_p
    print(f"  recovered m_a/m_b without the key: {ratio == expected}")


if __name__ == "__main__":
    main()
