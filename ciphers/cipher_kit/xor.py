"""Repeating-key XOR over bytes, and why a short or reused key is fatal.

``b ^ k ^ k == b``, so one function both encrypts and decrypts. With a short
key, every key-length-th byte shares one key byte, so the cipher splits into
single-byte XORs that each fall to a 256-way brute force.
"""

from itertools import cycle


def xor_bytes(data: bytes, key: bytes) -> bytes:
    """XOR ``data`` with ``key`` repeated; applying it twice gives ``data`` back."""
    if not key:
        raise ValueError("key must not be empty")
    return bytes(b ^ k for b, k in zip(data, cycle(key)))


def text_score(data: bytes) -> float:
    """Average per-byte plausibility as English text; higher is better."""
    if not data:
        return 0.0
    score = 0.0
    for b in data:
        if b == 32:
            score += 2.0
        elif 97 <= b <= 122:
            score += 1.0
        elif 65 <= b <= 90:
            score += 0.3
        elif b in (9, 10, 13) or 33 <= b < 127:
            score += 0.1
        else:
            score -= 5.0  # unprintable: almost certainly the wrong key
    return score / len(data)


def crack_single_byte_xor(data: bytes) -> tuple[int, bytes]:
    """Try all 256 one-byte keys; return (key byte, plaintext) that reads best."""
    best = max(range(256), key=lambda k: text_score(xor_bytes(data, bytes([k]))))
    return best, xor_bytes(data, bytes([best]))


def crack_repeating_xor(data: bytes, key_length: int) -> tuple[bytes, bytes]:
    """Recover (key, plaintext) for a known key length, one key byte per slice."""
    if key_length < 1:
        raise ValueError("key_length must be at least 1")
    key = bytes(crack_single_byte_xor(data[i::key_length])[0] for i in range(key_length))
    return key, xor_bytes(data, key)
