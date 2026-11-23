"""crypto_kit: SHA-256, HMAC, Merkle proofs, textbook RSA, Diffie-Hellman, Shamir sharing.

Toy / educational code, not for real security: use hashlib, hmac, secrets and
a reviewed library such as ``cryptography`` for anything that matters.

    >>> from crypto.crypto_kit import sha256, reconstruct_secret, split_secret
    >>> sha256(b"abc").hex()[:16]
    'ba7816bf8f01cfea'
    >>> shares = split_secret(1234, n=5, k=3)
    >>> reconstruct_secret(shares[1:4])
    1234
"""

from .hashing import MerkleTree, hmac_sha256, sha256, verify_proof
from .keys import (
    dh_keypair,
    dh_shared_secret,
    generate_prime,
    is_probable_prime,
    reconstruct_secret,
    rsa_decrypt,
    rsa_encrypt,
    rsa_keypair,
    rsa_sign,
    rsa_verify,
    split_secret,
)

__all__ = [
    "sha256",
    "hmac_sha256",
    "MerkleTree",
    "verify_proof",
    "is_probable_prime",
    "generate_prime",
    "rsa_keypair",
    "rsa_encrypt",
    "rsa_decrypt",
    "rsa_sign",
    "rsa_verify",
    "dh_keypair",
    "dh_shared_secret",
    "split_secret",
    "reconstruct_secret",
]
