"""Textbook RSA, Diffie-Hellman key exchange and Shamir secret sharing.

Toy / educational only: no padding, no constant-time arithmetic, small keys.
Every function takes an optional ``rng`` so demos and tests can be repeatable;
it defaults to ``secrets.SystemRandom()``.
"""

import random
import secrets
from math import gcd

# RFC 2409 group 1: a 768-bit safe prime with generator 2 (far too small today).
DH_PRIME = int(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DD"
    "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A63A3620FFFFFFFFFFFFFFFF",
    16,
)
DH_GENERATOR = 2
SHAMIR_PRIME = 2**521 - 1  # a Mersenne prime, larger than any secret we split

PublicKey = tuple[int, int]  # (e, n)
PrivateKey = tuple[int, int]  # (d, n)


def _rng(rng: random.Random | None) -> random.Random:
    return rng if rng is not None else secrets.SystemRandom()


def is_probable_prime(n: int, rounds: int = 20, rng: random.Random | None = None) -> bool:
    """Miller-Rabin: False means composite for sure, True means prime with high probability."""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    r = _rng(rng)
    for _ in range(rounds):
        x = pow(r.randrange(2, n - 1), d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits: int, rng: random.Random | None = None) -> int:
    """A random probable prime with exactly ``bits`` bits."""
    r = _rng(rng)
    while True:
        candidate = r.getrandbits(bits) | (1 << (bits - 1)) | 1  # top and bottom bits set
        if is_probable_prime(candidate, rng=r):
            return candidate


def rsa_keypair(bits: int = 256, rng: random.Random | None = None) -> tuple[PublicKey, PrivateKey]:
    """Two ``bits``-bit primes p, q; n = pq; d = e^-1 mod (p-1)(q-1)."""
    r = _rng(rng)
    p = generate_prime(bits, r)
    q = generate_prime(bits, r)
    while q == p:
        q = generate_prime(bits, r)
    phi = (p - 1) * (q - 1)
    e = 65537
    while gcd(e, phi) != 1:
        e += 2
    return (e, p * q), (pow(e, -1, phi), p * q)


def rsa_encrypt(message: int, public: PublicKey) -> int:
    """m^e mod n. Deterministic and malleable: this is why real RSA pads messages."""
    e, n = public
    if not 0 <= message < n:
        raise ValueError("message must be in range [0, n)")
    return pow(message, e, n)


def rsa_decrypt(cipher: int, private: PrivateKey) -> int:
    """c^d mod n, which gives back m by Euler's theorem."""
    d, n = private
    return pow(cipher, d, n)


def rsa_sign(message: int, private: PrivateKey) -> int:
    """Signing is 'decrypting' with the private key."""
    return rsa_decrypt(message, private)


def rsa_verify(message: int, signature: int, public: PublicKey) -> bool:
    """Anyone with the public key can check s^e mod n == m."""
    e, n = public
    return pow(signature, e, n) == message % n


def dh_keypair(p: int = DH_PRIME, g: int = DH_GENERATOR,
               rng: random.Random | None = None) -> tuple[int, int]:
    """A private exponent a and the public value g^a mod p to send to the other side."""
    secret = _rng(rng).randrange(2, p - 1)
    return secret, pow(g, secret, p)


def dh_shared_secret(their_public: int, my_secret: int, p: int = DH_PRIME) -> int:
    """(g^b)^a == (g^a)^b mod p: both sides compute the same number."""
    return pow(their_public, my_secret, p)


def split_secret(secret: int, n: int, k: int, prime: int = SHAMIR_PRIME,
                 rng: random.Random | None = None) -> list[tuple[int, int]]:
    """n points on a random degree-(k-1) polynomial whose constant term is ``secret``."""
    if not 0 <= secret < prime:
        raise ValueError("secret must be in range [0, prime)")
    if not 1 <= k <= n:
        raise ValueError("need 1 <= k <= n")
    r = _rng(rng)
    coeffs = [secret] + [r.randrange(prime) for _ in range(k - 1)]
    shares = []
    for x in range(1, n + 1):  # x = 0 would be the secret itself
        y = 0
        for c in reversed(coeffs):  # Horner's rule
            y = (y * x + c) % prime
        shares.append((x, y))
    return shares


def reconstruct_secret(shares: list[tuple[int, int]], prime: int = SHAMIR_PRIME) -> int:
    """Lagrange interpolation at x = 0; needs at least k shares to be right."""
    total = 0
    for i, (xi, yi) in enumerate(shares):
        num = den = 1
        for j, (xj, _) in enumerate(shares):
            if i != j:
                num = num * -xj % prime
                den = den * (xi - xj) % prime
        total = (total + yi * num * pow(den, -1, prime)) % prime
    return total
