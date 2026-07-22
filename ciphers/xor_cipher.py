"""XOR cipher: combine each byte of the message with a byte of the key.

Exclusive-or is its own inverse: (b ^ k) ^ k == b. That single property makes
encryption and decryption the same function, which is why xor sits underneath
almost every real stream cipher. Working on bytes rather than letters means any
data encrypts, not just text, so this file uses bytes throughout and shows the
result as hexadecimal.

With a truly random key as long as the message, used exactly once, xor is the
one-time pad and is provably unbreakable. Every one of those conditions matters.
A short repeating key turns the scheme into a Vigenere cipher over bytes and
falls to the same analysis. Worse, reusing one key for two messages hands the
attacker c1 ^ c2, which equals m1 ^ m2 with the key cancelled out entirely: the
key is gone and the two plaintexts can be teased apart by guessing common words.

Educational only, never for real security. Use hashlib and hmac for integrity,
and a reviewed library such as cryptography for encryption. Everything here is
O(n) time.
"""

from itertools import cycle


def xor_bytes(data: bytes, key: bytes) -> bytes:
    """Repeating-key xor. Being self-inverse, this both encrypts and decrypts."""
    if not key:
        raise ValueError("key must not be empty")
    return bytes(b ^ k for b, k in zip(data, cycle(key)))


def encrypt(text: str, key: str) -> bytes:
    return xor_bytes(text.encode("utf-8"), key.encode("utf-8"))


def decrypt(data: bytes, key: str) -> str:
    return xor_bytes(data, key.encode("utf-8")).decode("utf-8")


def hexdump(data: bytes) -> str:
    return data.hex()


def english_score(data: bytes) -> float:
    """Crude plausibility score. Spaces and lowercase letters dominate English,
    so rewarding them separates real text from merely printable noise."""
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
            score -= 5.0  # unprintable bytes mean the key is almost certainly wrong
    return score / len(data)


def crack_single_byte(data: bytes) -> tuple[int, bytes]:
    """A one-byte key has only 256 possibilities, so try them all."""
    best = max(range(256), key=lambda k: english_score(xor_bytes(data, bytes([k]))))
    return best, xor_bytes(data, bytes([best]))


def main() -> None:
    message = "meet me at the bridge at midnight"
    key = "s3cr3t"
    secret = encrypt(message, key)
    print(f"plaintext:  {message}")
    print(f"ciphertext: {hexdump(secret)}")
    print(f"decrypted:  {decrypt(secret, key)}")
    print(f"round trip ok: {decrypt(secret, key) == message}")

    # Encrypting twice with the same key returns the original bytes.
    twice = xor_bytes(xor_bytes(message.encode(), key.encode()), key.encode())
    print(f"double xor is identity: {twice == message.encode()}")
    print(f"empty message: {hexdump(encrypt('', key))!r}")
    try:
        xor_bytes(b"abc", b"")
    except ValueError as exc:
        print(f"empty key rejected: {exc}")

    print("single-byte key falls to brute force")
    weak = xor_bytes(b"the treasure is buried under the old oak tree", bytes([42]))
    found, recovered = crack_single_byte(weak)
    print(f"  key byte {found}, plaintext {recovered.decode()}")

    print("reusing a one-time pad across two messages")
    pad = bytes(range(1, 21))  # a fixed 'random' pad, 20 bytes
    m1 = b"attack at dawn......"
    m2 = b"retreat at dusk....."
    c1 = xor_bytes(m1, pad)
    c2 = xor_bytes(m2, pad)
    print(f"  c1 = {hexdump(c1)}")
    print(f"  c2 = {hexdump(c2)}")
    leaked = xor_bytes(c1, c2)
    print(f"  c1 ^ c2      = {hexdump(leaked)}")
    print(f"  m1 ^ m2      = {hexdump(xor_bytes(m1, m2))}")
    print(f"  pad cancels: {leaked == xor_bytes(m1, m2)}")
    # Knowing or guessing one plaintext instantly reveals the other.
    print(f"  guess m1, recover m2: {xor_bytes(leaked, m1).decode()!r}")


if __name__ == "__main__":
    main()
