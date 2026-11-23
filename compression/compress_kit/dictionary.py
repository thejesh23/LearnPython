"""Dictionary coders: LZ77 copies from a sliding window, LZW grows a phrase table.

Both replace repeated substrings with short references. LZ77 points back into
text it has already produced; LZW numbers every phrase it has seen, and the
decoder rebuilds the same numbering on its own, so no table is ever sent.
"""

from typing import NamedTuple


class Token(NamedTuple):
    """Copy ``length`` chars from ``offset`` back, then emit ``char``."""

    offset: int
    length: int
    char: str


def lz77_compress(text: str, window: int = 255, lookahead: int = 15) -> list[Token]:
    """Greedy LZ77: at each step take the longest match in the last ``window`` chars."""
    tokens: list[Token] = []
    i, n = 0, len(text)
    while i < n:
        best_off = best_len = 0
        for j in range(max(0, i - window), i):
            length = 0
            # Stop one short of the end so every token still carries a literal.
            while length < lookahead and i + length < n - 1 and text[j + length] == text[i + length]:
                length += 1
            if length > best_len:
                best_off, best_len = i - j, length
        tokens.append(Token(best_off, best_len, text[i + best_len]))
        i += best_len + 1
    return tokens


def lz77_decompress(tokens: list[Token]) -> str:
    """Replay the copies; one char at a time so a copy may overlap its own output."""
    out: list[str] = []
    for offset, length, char in tokens:
        start = len(out) - offset
        for k in range(length):
            out.append(out[start + k])
        out.append(char)
    return "".join(out)


def lzw_encode(text: str) -> list[int]:
    """Emit the code of the longest known phrase, then learn phrase + next char.

    The table starts with the 256 Latin-1 characters, so every char must be < 256.
    """
    table = {chr(i): i for i in range(256)}
    out: list[int] = []
    phrase = ""
    for ch in text:
        if ord(ch) > 255:
            raise ValueError(f"LZW here handles Latin-1 text only, got {ch!r}")
        if phrase + ch in table:
            phrase += ch
        else:
            out.append(table[phrase])
            table[phrase + ch] = len(table)
            phrase = ch
    if phrase:
        out.append(table[phrase])
    return out


def lzw_decode(codes: list[int]) -> str:
    """Rebuild the encoder's table one step behind it (with the KwKwK special case)."""
    if not codes:
        return ""
    table = {i: chr(i) for i in range(256)}
    prev = table[codes[0]]
    out = [prev]
    for code in codes[1:]:
        if code in table:
            entry = table[code]
        elif code == len(table):
            entry = prev + prev[0]  # the encoder made this entry on the very last step
        else:
            raise ValueError(f"bad LZW code {code}")
        out.append(entry)
        table[len(table)] = prev + entry[0]
        prev = entry
    return "".join(out)
