"""Hashes, message signatures, random tokens and password storage.

A *hash function* turns any amount of data into a short, fixed-size
fingerprint. The same input always gives the same fingerprint, a one-byte
change gives a completely different one, and you cannot work backwards from
the fingerprint to the data. Each job below needs a different tool:

    hashlib.sha256         check a download or detect a changed file
    hmac                   prove a message came from someone with the key
    secrets                unguessable tokens, reset links, API keys
    hashlib.scrypt or      store passwords: deliberately slow, with a
    hashlib.pbkdf2_hmac    random salt per password

Two traps: the `random` module is predictable and must never make tokens or
passwords, and comparing secrets with `==` can leak, through timing, how much
of a guess was right. Use `secrets` and `hmac.compare_digest` instead.

Values from `secrets` change every run, so this file prints their length and
shape rather than the values themselves.
"""

import hashlib
import hmac
import random
import secrets
import string
import tempfile
from pathlib import Path


def sha256_demo() -> None:
    # Hash functions work on bytes, so encode text first.
    digest = hashlib.sha256(b"hello world").hexdigest()
    print(f"sha256('hello world')  = {digest}")
    print(f"sha256('hello world!') = {hashlib.sha256(b'hello world!').hexdigest()}")
    # One extra character changed the whole fingerprint.
    print(f"always {len(digest)} hex characters = 256 bits, whatever the input size")

    # update() feeds data in pieces; the result is the same as all at once.
    h = hashlib.sha256()
    h.update(b"hello ")
    h.update(b"world")
    print(f"piece by piece matches: {h.hexdigest() == digest}")

    # MD5 and SHA-1 are broken for security (collisions can be made on
    # purpose). They are still fine as quick checksums when no attacker is
    # involved; usedforsecurity=False says so explicitly.
    md5 = hashlib.md5(b"hello world", usedforsecurity=False).hexdigest()
    print(f"md5 (checksum only)    = {md5}")


def hash_file(path: Path, chunk_size: int = 64 * 1024) -> str:
    """Hash a file of any size while holding only one chunk in memory."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        # iter(callable, sentinel) calls f.read until it returns b"" (the end).
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def file_hash_demo() -> None:
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "download.bin"
        path.write_bytes(bytes(range(256)) * 4096)  # 1 MiB of sample data
        ours = hash_file(path)
        print(f"sha256 of the 1 MiB file: {ours[:16]}...")

        # Python 3.11+ has hashlib.file_digest, which does the same loop.
        with path.open("rb") as f:
            builtin = hashlib.file_digest(f, "sha256").hexdigest()
        print(f"hashlib.file_digest agrees: {builtin == ours}")

        # A download page publishes the expected hash; compare against it.
        expected = ours
        with path.open("r+b") as f:
            f.seek(500_000)
            f.write(b"\xff")  # one corrupted byte in the middle
        print(f"after one corrupted byte, still matches: {hash_file(path) == expected}")


def sign(key: bytes, message: bytes) -> str:
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def verify(key: bytes, message: bytes, signature: str) -> bool:
    # compare_digest takes the same time whether the first or the last
    # character differs, so an attacker cannot guess one character at a time.
    return hmac.compare_digest(sign(key, message), signature)


def hmac_demo() -> None:
    # Imagine a web server signing a cookie so a user cannot edit it.
    key = b"server-side secret key, never sent to users"
    cookie = b"user=ana;role=member"
    signature = sign(key, cookie)
    print(f"cookie: {cookie.decode()}  signature: {signature[:16]}...")
    print(f"unchanged cookie verifies:   {verify(key, cookie, signature)}")

    # The user edits the cookie but cannot make a new signature without the key.
    forged = b"user=ana;role=admin"
    print(f"edited cookie verifies:      {verify(key, forged, signature)}")
    print(f"right data, wrong key:       {verify(b'guess', cookie, signature)}")
    # A plain sha256(key + message) is NOT a safe substitute for hmac.


def make_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + "-_.!"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def secrets_demo() -> None:
    # Each call gives a fresh value from the operating system's secure source.
    hex_token = secrets.token_hex(16)        # 16 random bytes as 32 hex chars
    url_token = secrets.token_urlsafe(32)    # safe inside a URL
    print(f"token_hex(16):     {len(hex_token)} chars, all hex: "
          f"{all(c in string.hexdigits for c in hex_token)}")
    print(f"token_urlsafe(32): {len(url_token)} chars, no '/' or '+': "
          f"{'/' not in url_token and '+' not in url_token}")
    print(f"two tokens differ: {secrets.token_hex(16) != secrets.token_hex(16)}")
    print(f"a 6-digit code:    {len(f'{secrets.randbelow(10**6):06d}')} digits")
    print(f"make_password():   {len(make_password())} characters")

    # random is built for simulations: fast and *reproducible*. Anyone who
    # learns or guesses the seed (or sees enough outputs) can predict it.
    victim = random.Random(2026)
    reset_code = victim.randrange(10**6)
    attacker = random.Random(2026)
    print(f"attacker with the same seed predicts the code: "
          f"{attacker.randrange(10**6) == reset_code}")


# scrypt cost settings: n=2**14, r=8 uses 16 MiB of memory per guess, which
# makes large-scale guessing on graphics cards expensive.
SCRYPT_N, SCRYPT_R, SCRYPT_P = 2**14, 8, 1


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)  # a new random salt for every password
    key = hashlib.scrypt(password.encode(), salt=salt,
                         n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P)
    # Store the settings and salt next to the hash; none of them are secret.
    return f"scrypt${SCRYPT_N}${SCRYPT_R}${SCRYPT_P}${salt.hex()}${key.hex()}"


def check_password(password: str, stored: str) -> bool:
    _, n, r, p, salt_hex, key_hex = stored.split("$")
    key = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt_hex),
                         n=int(n), r=int(r), p=int(p))
    return hmac.compare_digest(key.hex(), key_hex)


def password_demo() -> None:
    # Never store passwords, and never store a plain sha256 of them: it is so
    # fast that billions of guesses per second are possible.
    stored = hash_password("correct horse battery staple")
    name, n, r, p, salt_hex, key_hex = stored.split("$")
    print(f"stored record: {name}${n}${r}${p}$<{len(salt_hex)} hex salt>"
          f"$<{len(key_hex)} hex hash>")
    print(f"right password: {check_password('correct horse battery staple', stored)}")
    print(f"wrong password: {check_password('Tr0ub4dor&3', stored)}")

    # The salt makes equal passwords hash differently, so one precomputed
    # table cannot crack every user at once.
    again = hash_password("correct horse battery staple")
    print(f"same password, different record: {again != stored}")

    # PBKDF2 is the older, widely supported choice. Its strength comes from
    # repeating the hash many times; 600_000 is a current recommendation.
    salt = secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac("sha256", b"correct horse", salt, 600_000)
    print(f"pbkdf2_hmac with 600_000 rounds -> {len(key)}-byte key")


def main() -> None:
    sha256_demo()
    print()
    file_hash_demo()
    print()
    hmac_demo()
    print()
    secrets_demo()
    print()
    password_demo()


if __name__ == "__main__":
    main()
