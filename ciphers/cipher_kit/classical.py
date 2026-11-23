"""Letter ciphers: Caesar and Vigenere, plus the frequency analysis that breaks them.

Both shift letters around a 26-letter alphabet and leave everything else alone.
A Vigenere cipher with a key of length m is just m interleaved Caesar ciphers,
so cracking it reuses the Caesar cracker on every m-th letter.
"""

ALPHABET_SIZE = 26

# Relative frequency (percent) of each letter in ordinary English, A through Z.
ENGLISH_FREQ = [
    8.17, 1.49, 2.78, 4.25, 12.70, 2.23, 2.02, 6.09, 6.97, 0.15, 0.77, 4.03,
    2.41, 6.75, 7.51, 1.93, 0.10, 5.99, 6.33, 9.06, 2.76, 0.98, 2.36, 0.15,
    1.97, 0.07,
]


def _shift(ch: str, key: int) -> str:
    if "a" <= ch <= "z":
        base = ord("a")
    elif "A" <= ch <= "Z":
        base = ord("A")
    else:
        return ch
    return chr(base + (ord(ch) - base + key) % ALPHABET_SIZE)


def _letters(text: str) -> str:
    return "".join(c for c in text.lower() if "a" <= c <= "z")


def caesar_encrypt(text: str, key: int) -> str:
    """Shift every letter ``key`` places forward, keeping case and non-letters."""
    return "".join(_shift(c, key) for c in text)


def caesar_decrypt(text: str, key: int) -> str:
    """Undo ``caesar_encrypt`` by shifting the other way."""
    return caesar_encrypt(text, -key)


def english_score(text: str) -> float:
    """Chi-squared distance from English letter frequencies; lower is more English."""
    letters = _letters(text)
    if not letters:
        return float("inf")
    counts = [0] * ALPHABET_SIZE
    for c in letters:
        counts[ord(c) - ord("a")] += 1
    expected = [f * len(letters) / 100 for f in ENGLISH_FREQ]
    return sum((got - exp) ** 2 / exp for got, exp in zip(counts, expected))


def crack_caesar(text: str) -> tuple[int, str]:
    """Try all 26 keys and return the (key, plaintext) that looks most English."""
    return min(
        ((k, caesar_decrypt(text, k)) for k in range(ALPHABET_SIZE)),
        key=lambda kv: english_score(kv[1]),
    )


def _vigenere(text: str, key: str, sign: int) -> str:
    shifts = [ord(c) - ord("a") for c in _letters(key)]
    if not shifts:
        raise ValueError("key must contain at least one letter")
    out, k = [], 0
    for ch in text:
        if ch.isascii() and ch.isalpha():
            out.append(_shift(ch, sign * shifts[k % len(shifts)]))
            k += 1  # only letters use up the key
        else:
            out.append(ch)
    return "".join(out)


def vigenere_encrypt(text: str, key: str) -> str:
    """Shift each letter by the matching letter of the repeating ``key``."""
    return _vigenere(text, key, 1)


def vigenere_decrypt(text: str, key: str) -> str:
    """Undo ``vigenere_encrypt`` with the same key."""
    return _vigenere(text, key, -1)


def index_of_coincidence(text: str) -> float:
    """Chance two random letters of ``text`` match: ~0.066 for English, ~0.038 for noise."""
    letters = _letters(text)
    n = len(letters)
    if n < 2:
        return 0.0
    return sum(letters.count(c) * (letters.count(c) - 1) for c in set(letters)) / (n * (n - 1))


def guess_key_length(text: str, max_length: int = 12) -> int:
    """Smallest key length whose every-m-th-letter slices look like English.

    The right length (and its multiples) makes each slice a plain Caesar
    cipher, so its average index of coincidence jumps up to English levels.
    """
    letters = _letters(text)
    scores = []
    for m in range(1, max_length + 1):
        slices = [letters[i::m] for i in range(m)]
        scores.append(sum(map(index_of_coincidence, slices)) / m)
    best = max(scores)
    return next(m for m, s in enumerate(scores, 1) if s >= 0.9 * best)


def crack_vigenere(text: str, key_length: int | None = None) -> tuple[str, str]:
    """Recover (key, plaintext): guess the key length, then crack each slice as Caesar."""
    m = key_length or guess_key_length(text)
    letters = _letters(text)
    key = "".join(chr(ord("a") + crack_caesar(letters[i::m])[0]) for i in range(m))
    return key, vigenere_decrypt(text, key)
