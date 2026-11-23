"""Examples and self-check: python3 -m compression.compress_kit"""

import random
import sys
import zlib

from . import (
    CODECS,
    bwt,
    compress,
    decompress,
    huffman_codes,
    huffman_encode,
    lz77_compress,
    lzw_encode,
    pack_ints,
    unpack_ints,
)

TEXT = "the rain in spain stays mainly in the plain; " * 4


def longest_run(s: str) -> int:
    best = run = 0
    for i, ch in enumerate(s):
        run = run + 1 if i and ch == s[i - 1] else 1
        best = max(best, run)
    return best


def examples() -> None:
    print("1. huffman codes for 'abracadabra':", huffman_codes("abracadabra"))
    payload = huffman_encode(TEXT)
    print(f"2. huffman: {len(TEXT) * 8} bits -> {payload.bit_count} bits")
    tokens = lz77_compress(TEXT)
    print(f"3. lz77: {len(TEXT)} chars -> {len(tokens)} tokens, last {tuple(tokens[-1])}")
    codes = lzw_encode(TEXT)
    print(f"4. lzw: {len(TEXT)} chars -> {len(codes)} codes (12 bits each: {len(codes) * 12} bits)")
    print("5. lzw KwKwK case 'aaaaaa' ->", lzw_encode("aaaaaa"))
    shown = bwt("banana").replace("\x00", "$")
    print(f"6. bwt('banana') = {shown!r}; longest run in TEXT "
          f"{longest_run(TEXT)} -> {longest_run(bwt(TEXT))}")
    ids = list(range(4_000_000, 4_002_000, 3))
    print(f"7. {len(ids)} sorted ids: {len(ids) * 4} bytes as uint32 -> {len(pack_ints(ids))} bytes packed")
    zipped = zlib.compress(TEXT.encode(), 9)
    print(f"8. for scale, zlib (LZ77 + Huffman) on TEXT: {len(TEXT)} -> {len(zipped)} bytes")


def self_check() -> None:
    rng = random.Random(3)
    alphabets = ["a", "ab", "abc ", "the quick brown fox", "".join(map(chr, range(1, 256)))]
    samples = ["", "a", "aaaaaa", "abababab", "TOBEORNOTTOBEORTOBEORNOT", TEXT]
    for _ in range(120):
        alphabet = rng.choice(alphabets)
        samples.append("".join(rng.choice(alphabet) for _ in range(rng.randint(0, 150))))
    for text in samples:
        for method in CODECS:
            assert decompress(compress(text, method), method) == text, (method, text)
        window, lookahead = rng.randint(1, 40), rng.randint(1, 10)
        assert decompress(lz77_compress(text, window, lookahead), "lz77") == text
        codes = huffman_codes(text)
        assert set(codes) == set(text)
        assert not any(a != b and b.startswith(a) for a in codes.values() for b in codes.values())
        if len(set(text)) > 1:  # optimal codes fill the Kraft inequality exactly
            assert sum(2 ** -len(c) for c in codes.values()) == 1
    for _ in range(200):
        size = 10 ** rng.randint(0, 20)
        values = [rng.randint(-size, size) for _ in range(rng.randint(0, 30))]
        assert unpack_ints(pack_ints(values)) == values
    assert len(pack_ints([127])) == 2 and len(pack_ints([63])) == 1  # zigzag doubles: 127 -> 254
    for bad in (lambda: lzw_encode("snow ☃"), lambda: bwt("a\x00b"), lambda: unpack_ints(b"\x80"),
                lambda: compress("x", "zip")):
        try:
            bad()
        except ValueError:
            pass
        else:
            raise AssertionError("bad input accepted")


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
