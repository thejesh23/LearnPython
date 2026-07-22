"""Vigenere cipher: a Caesar shift whose key changes letter by letter.

Take a keyword, repeat it across the message, and shift each plaintext letter by
the alphabet position of the key letter above it. For three centuries this was
considered unbreakable, because the same plaintext letter encrypts to different
ciphertext letters depending on where it falls, which flattens the letter
frequencies that break a Caesar cipher.

The flaw is that the key repeats. If the key has length m, then positions 0, m,
2m and so on are all encrypted with the same shift, so the ciphertext is really
m interleaved Caesar ciphers. Kasiski's observation makes finding m easy: when a
common word lines up with the same part of the key twice, it produces an
identical ciphertext chunk, and the distance between such repeats is almost
always a multiple of the key length. Take the greatest common divisor of those
distances to recover m, then break each of the m slices by frequency analysis.

Historical and educational only. Never use this for real security. Use hashlib
and hmac for integrity, and a reviewed library such as cryptography for actual
encryption. Encrypting and decrypting are O(n).
"""

from math import gcd

ALPHABET_SIZE = 26


def _clean_key(key: str) -> list[int]:
    shifts = [ord(c.lower()) - ord("a") for c in key if c.isalpha()]
    if not shifts:
        raise ValueError("key must contain at least one letter")
    return shifts


def _apply(text: str, key: str, sign: int) -> str:
    shifts = _clean_key(key)
    out: list[str] = []
    k = 0  # advances only on letters, so punctuation does not consume the key
    for ch in text:
        if "a" <= ch <= "z":
            base = ord("a")
        elif "A" <= ch <= "Z":
            base = ord("A")
        else:
            out.append(ch)
            continue
        shift = sign * shifts[k % len(shifts)]
        out.append(chr(base + (ord(ch) - base + shift) % ALPHABET_SIZE))
        k += 1
    return "".join(out)


def encrypt(text: str, key: str) -> str:
    return _apply(text, key, 1)


def decrypt(text: str, key: str) -> str:
    return _apply(text, key, -1)


def repeated_sequence_spacings(text: str, length: int = 3) -> dict[str, list[int]]:
    """Kasiski step one: distances between repeats of each n-gram."""
    letters = [c.lower() for c in text if c.isalpha()]
    positions: dict[str, list[int]] = {}
    for i in range(len(letters) - length + 1):
        positions.setdefault("".join(letters[i:i + length]), []).append(i)
    spacings: dict[str, list[int]] = {}
    for gram, idxs in positions.items():
        if len(idxs) > 1:
            spacings[gram] = [idxs[j] - idxs[0] for j in range(1, len(idxs))]
    return spacings


def guess_key_length(text: str, length: int = 3) -> int | None:
    """Kasiski step two: the gcd of all repeat spacings is a multiple of the key."""
    all_spacings: list[int] = []
    for gaps in repeated_sequence_spacings(text, length).values():
        all_spacings.extend(gaps)
    if not all_spacings:
        return None
    guess = 0
    for gap in all_spacings:
        guess = gcd(guess, gap)
    return guess or None


def main() -> None:
    message = "The quick brown fox jumps over the lazy dog."
    key = "LEMON"
    secret = encrypt(message, key)
    print(f"plaintext:  {message}")
    print(f"key:        {key}")
    print(f"ciphertext: {secret}")
    print(f"decrypted:  {decrypt(secret, key)}")
    print(f"round trip ok: {decrypt(secret, key) == message}")

    # A one-letter key is exactly a Caesar cipher.
    print(f"key 'd' is Caesar 3: {encrypt('attack', 'd')}")
    print(f"key 'a' is a no-op:  {encrypt(message, 'a') == message}")
    print(f"empty text:          {encrypt('', key)!r}")
    print(f"mixed case kept:     {encrypt('AbC', 'ab')}")
    try:
        encrypt("hello", "1234")
    except ValueError as exc:
        print(f"non-letter key rejected: {exc}")

    # Key reuse leaks structure: the same word at the same key offset repeats.
    plain = "attack attack attack attack"
    leaky = encrypt(plain, "key")
    print(f"repeating plaintext: {plain}")
    print(f"repeating cipher:    {leaky}")
    spacings = repeated_sequence_spacings(leaky)
    shown = sorted(spacings.items())[:3]
    print(f"repeated trigrams: {shown}")
    # The gcd is a multiple of the key length, not always the length itself:
    # here the plaintext also repeats every six letters, so 6 comes out.
    print(f"gcd of spacings: {guess_key_length(leaky)} (key length 3 divides it)")
    print(f"no repeats found:  {guess_key_length('abcdef')}")


if __name__ == "__main__":
    main()
