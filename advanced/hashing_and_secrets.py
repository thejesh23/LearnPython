"""Hashing, HMAC, and generating secrets — the right tool per job.

Three different jobs, three different primitives:
    hashlib.sha256      integrity and content addressing. Fast, and therefore
                        wrong for passwords.
    hashlib.scrypt      password storage. Deliberately slow and memory-hard,
                        with a per-password random salt.
    hmac.new            message authentication with a shared key: proves the
                        message came from someone holding the key.

Two rules: compare secrets with `hmac.compare_digest` (constant time, so timing
does not leak how much of the value matched), and generate tokens with
`secrets`, never `random` — the latter is a predictable PRNG.
"""

import hashlib
import hmac
import secrets


def hash_password(password: str) -> tuple[bytes, bytes]:
    salt = secrets.token_bytes(16)  # unique per password, stored alongside
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return salt, digest


def verify_password(password: str, salt: bytes, expected: bytes) -> bool:
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return hmac.compare_digest(digest, expected)  # constant time


def sign(message: bytes, key: bytes) -> str:
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def main() -> None:
    data = b"the quick brown fox"
    print(f"sha256:  {hashlib.sha256(data).hexdigest()}")
    print(f"blake2b: {hashlib.blake2b(data, digest_size=16).hexdigest()}")
    print(f"one bit changed -> {hashlib.sha256(b'the quick brown box').hexdigest()[:32]}...")

    # Streaming, for data that does not fit in memory.
    hasher = hashlib.sha256()
    for chunk in (b"the ", b"quick ", b"brown ", b"fox"):
        hasher.update(chunk)
    print(f"streamed equals one-shot: {hasher.hexdigest() == hashlib.sha256(data).hexdigest()}")

    print("\npassword storage:")
    salt, stored = hash_password("correct horse battery staple")
    print(f"  salt {salt.hex()[:16]}... digest {stored.hex()[:16]}...")
    print(f"  correct password -> {verify_password('correct horse battery staple', salt, stored)}")
    print(f"  wrong password   -> {verify_password('hunter2', salt, stored)}")
    salt2, stored2 = hash_password("correct horse battery staple")
    print(f"  same password, different salt -> different digest: {stored != stored2}")

    print("\nHMAC:")
    key = secrets.token_bytes(32)
    message = b"amount=100&to=alice"
    signature = sign(message, key)
    print(f"  signature: {signature[:32]}...")
    print(f"  verifies:  {hmac.compare_digest(signature, sign(message, key))}")
    tampered = b"amount=100000&to=mallory"
    print(f"  tampered:  {hmac.compare_digest(signature, sign(tampered, key))}")

    print("\nsecrets, not random:")
    print(f"  token_hex(16):    {secrets.token_hex(16)}")
    print(f"  token_urlsafe(16):{secrets.token_urlsafe(16)}")
    print(f"  choice:           {secrets.choice(['a', 'b', 'c'])}")
    print(f"  randbelow(100):   {secrets.randbelow(100)}")
    print("  random.random() is a Mersenne Twister: reproducible, and predictable "
          "from enough output")

    print("\nmd5/sha1 are broken for security; keep them only for non-adversarial checksums")


if __name__ == "__main__":
    main()
