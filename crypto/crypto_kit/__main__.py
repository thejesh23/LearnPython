"""Examples and self-check: python3 -m crypto.crypto_kit"""

import hashlib
import hmac
import random
import sys

from . import (
    MerkleTree,
    dh_keypair,
    dh_shared_secret,
    generate_prime,
    hmac_sha256,
    is_probable_prime,
    reconstruct_secret,
    rsa_decrypt,
    rsa_encrypt,
    rsa_keypair,
    rsa_sign,
    rsa_verify,
    sha256,
    split_secret,
    verify_proof,
)


def examples() -> None:
    rng = random.Random(2024)  # repeatable demo; real keys need secrets
    print("1. sha256('abc'):", sha256(b"abc").hex())
    a, b = sha256(b"message"), sha256(b"messagf")
    changed = sum(bin(x ^ y).count("1") for x, y in zip(a, b))
    print("2. one bit flipped ->", changed, "of 256 digest bits change")
    tag = hmac_sha256(b"key", b"transfer $100 to Alice")
    print("3. hmac tag:", tag.hex()[:32] + "...", "| tampered message passes:",
          hmac.compare_digest(tag, hmac_sha256(b"key", b"transfer $900 to Mallory")))
    tree = MerkleTree([f"tx {i}".encode() for i in range(8)])
    proof = tree.proof(3)
    print("4. merkle proof for tx 3:", len(proof), "hashes",
          "| valid:", verify_proof(b"tx 3", proof, tree.root),
          "| forged:", verify_proof(b"tx 999", proof, tree.root))
    public, private = rsa_keypair(128, rng)
    m = int.from_bytes(b"hello", "big")
    print("5. RSA n has", public[1].bit_length(), "bits",
          "| round trip:", rsa_decrypt(rsa_encrypt(m, public), private) == m)
    sig = rsa_sign(m, private)
    print("6. RSA signature verifies:", rsa_verify(m, sig, public),
          "| on m+1:", rsa_verify(m + 1, sig, public))
    (a_secret, a_public), (b_secret, b_public) = dh_keypair(rng=rng), dh_keypair(rng=rng)
    agree = dh_shared_secret(b_public, a_secret) == dh_shared_secret(a_public, b_secret)
    print("7. Diffie-Hellman both sides agree:", agree)
    shares = split_secret(int.from_bytes(b"launch code", "big"), n=5, k=3, rng=rng)
    got = reconstruct_secret([shares[0], shares[2], shares[4]])
    print("8. Shamir 3 of 5 shares ->", got.to_bytes(11, "big"),
          "| 2 shares recover it:", reconstruct_secret(shares[:2]) == got)


def self_check() -> None:
    rng = random.Random(11)
    for size in [0, 1, 55, 56, 63, 64, 65, 119, 120, 128] + [rng.randrange(300) for _ in range(60)]:
        data = rng.randbytes(size)
        assert sha256(data) == hashlib.sha256(data).digest(), size
        key = rng.randbytes(rng.choice([0, 5, 64, 65, 150]))
        assert hmac_sha256(key, data) == hmac.new(key, data, hashlib.sha256).digest(), (size, len(key))
    for n in range(1, 18):
        items = [rng.randbytes(4) for _ in range(n)]
        tree = MerkleTree(items)
        assert all(verify_proof(item, tree.proof(i), tree.root) for i, item in enumerate(items))
        assert not verify_proof(b"not in the tree", tree.proof(0), tree.root)
    small_primes = [p for p in range(2, 2000) if all(p % d for d in range(2, int(p**0.5) + 1))]
    assert [n for n in range(2000) if is_probable_prime(n, rng=rng)] == small_primes
    assert generate_prime(40, rng).bit_length() == 40
    for _ in range(5):
        public, private = rsa_keypair(64, rng)
        for _ in range(20):
            m = rng.randrange(public[1])
            assert rsa_decrypt(rsa_encrypt(m, public), private) == m
            assert rsa_verify(m, rsa_sign(m, private), public)
    a, b = dh_keypair(rng=rng), dh_keypair(rng=rng)
    assert dh_shared_secret(b[1], a[0]) == dh_shared_secret(a[1], b[0])
    for _ in range(30):
        secret, k = rng.randrange(10**30), rng.randint(1, 6)
        shares = split_secret(secret, n=k + 3, k=k, rng=rng)
        assert reconstruct_secret(rng.sample(shares, k)) == secret
        if k > 1:
            assert reconstruct_secret(rng.sample(shares, k - 1)) != secret


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
