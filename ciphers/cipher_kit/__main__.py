"""Examples and self-check: python3 -m ciphers.cipher_kit"""

import random
import string
import sys

from . import (
    caesar_decrypt,
    caesar_encrypt,
    crack_caesar,
    crack_repeating_xor,
    crack_single_byte_xor,
    crack_vigenere,
    guess_key_length,
    index_of_coincidence,
    vigenere_decrypt,
    vigenere_encrypt,
    xor_bytes,
)

PASSAGE = (
    "It was the best of times, it was the worst of times, it was the age of wisdom, "
    "it was the age of foolishness, it was the epoch of belief, it was the epoch of "
    "incredulity, it was the season of light, it was the season of darkness, it was "
    "the spring of hope, it was the winter of despair, we had everything before us, "
    "we had nothing before us, we were all going direct to heaven, we were all going "
    "direct the other way. In short, the period was so far like the present period, "
    "that some of its noisiest authorities insisted on its being received, for good "
    "or for evil, in the superlative degree of comparison only."
)


def examples() -> None:
    secret = caesar_encrypt("Attack at dawn, bring the ninth legion!", 3)
    print("1. caesar key 3:", secret, "->", caesar_decrypt(secret, 3))
    print("2. caesar cracked with no key:", crack_caesar(caesar_encrypt(PASSAGE[:80], 11)))
    v = vigenere_encrypt(PASSAGE, "dickens")
    print("3. vigenere 'dickens':", v[:46] + "...")
    print("4. index of coincidence: English %.3f, vigenere %.3f"
          % (index_of_coincidence(PASSAGE), index_of_coincidence(v)))
    key, plain = crack_vigenere(v)
    print("5. key length guess:", guess_key_length(v), "| cracked key:", key, "|", plain[:30] + "...")
    weak = xor_bytes(b"the treasure is buried under the old oak tree", bytes([42]))
    print("6. single-byte xor cracked:", crack_single_byte_xor(weak))
    m1, m2, pad = b"attack at dawn", b"retreat at six", b"pad!pad!pad!pa"
    c1, c2 = xor_bytes(m1, pad), xor_bytes(m2, pad)
    print("7. reused pad, c1 ^ c2 == m1 ^ m2:", xor_bytes(c1, c2) == xor_bytes(m1, m2))
    rk, rp = crack_repeating_xor(xor_bytes(PASSAGE.encode(), b"ICE"), 3)
    print("8. repeating xor, key length 3:", rk, "|", rp[:30])


def self_check() -> None:
    rng = random.Random(23)
    alphabet = string.ascii_letters + string.digits + " ,.!?-"
    for _ in range(200):
        text = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 60)))
        k = rng.randint(-100, 100)
        key = "".join(rng.choice(string.ascii_letters) for _ in range(rng.randint(1, 8)))
        raw = rng.randbytes(rng.randint(1, 6))
        assert caesar_decrypt(caesar_encrypt(text, k), k) == text
        assert caesar_encrypt(text, k) == caesar_encrypt(text, k % 26)
        assert vigenere_decrypt(vigenere_encrypt(text, key), key) == text
        assert xor_bytes(xor_bytes(text.encode(), raw), raw) == text.encode()
    assert vigenere_encrypt("attack", "d") == caesar_encrypt("attack", 3)
    for _ in range(10):
        k = rng.randrange(26)
        assert crack_caesar(caesar_encrypt(PASSAGE, k)) == (k, PASSAGE)
        key = "".join(rng.choice(string.ascii_lowercase) for _ in range(rng.randint(3, 6)))
        found, plain = crack_vigenere(vigenere_encrypt(PASSAGE, key))
        assert plain == PASSAGE and len(found) % len(key) == 0, (key, found)
        raw = bytes(rng.randrange(256) for _ in range(rng.randint(2, 5)))
        assert crack_repeating_xor(xor_bytes(PASSAGE.encode(), raw), len(raw)) == (raw, PASSAGE.encode())
    for bad in (lambda: vigenere_encrypt("x", "123"), lambda: xor_bytes(b"x", b"")):
        try:
            bad()
        except ValueError:
            pass
        else:
            raise AssertionError("bad key accepted")


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
