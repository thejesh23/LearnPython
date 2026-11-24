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


def main() -> None:
    sha256_demo()
    print()
    file_hash_demo()


if __name__ == "__main__":
    main()
