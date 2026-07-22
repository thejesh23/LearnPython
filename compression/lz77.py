"""LZ77: describe the next bytes as "copy from what we already decoded".

The compressor keeps a sliding window of recently seen text and a lookahead
buffer of text still to come. At each step it searches the window for the
longest prefix of the lookahead and emits a token (offset, length, next_char),
where offset counts backwards from the current position. A literal is just the
token (0, 0, char). The decompressor needs no dictionary at all: it copies
length bytes from offset back in its own output.

The two buffer sizes are the whole trade. A bigger window finds more distant
matches but costs more bits per offset and more search time; a bigger lookahead
allows longer copies but again more bits per length. DEFLATE (gzip, zlib, PNG)
is exactly this with a 32 KB window, plus Huffman coding of the tokens.

Copies may overlap the current position, which is how runs get encoded cheaply.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    offset: int
    length: int
    char: str


def compress(text: str, window: int = 20, lookahead: int = 8) -> list[Token]:
    tokens: list[Token] = []
    i = 0
    n = len(text)
    while i < n:
        best_off = best_len = 0
        start = max(0, i - window)
        # Search the window for the longest match; ties go to the nearest one.
        for j in range(start, i):
            length = 0
            while (
                length < lookahead
                and i + length < n - 1  # leave one char for the literal
                and text[j + length] == text[i + length]
            ):
                length += 1
            if length > best_len:
                best_off, best_len = i - j, length
        tokens.append(Token(best_off, best_len, text[i + best_len]))
        i += best_len + 1
    return tokens


def decompress(tokens: list[Token]) -> str:
    out: list[str] = []
    for tok in tokens:
        start = len(out) - tok.offset
        for k in range(tok.length):
            out.append(out[start + k])  # one char at a time: copies may overlap
        out.append(tok.char)
    return "".join(out)


def ratio(text: str, tokens: list[Token]) -> str:
    """Charge 5 bits offset + 3 bits length + 8 bits literal per token."""
    if not text:
        return "n/a (empty input)"
    before, after = len(text) * 8, len(tokens) * 16
    return f"{before} bits -> {after} bits ({after / before:.2f}x)"


def main() -> None:
    samples = [
        "",
        "abracadabra abracadabra",
        "aaaaaaaaaaaaaaaa",
        "xyzw",  # nothing to match: every token is a literal, so it expands
    ]
    for text in samples:
        tokens = compress(text)
        back = decompress(tokens)
        print(f"input     : {text!r}")
        print(f"tokens    : {[(t.offset, t.length, t.char) for t in tokens]}")
        print(f"round-trip: {back == text}")
        print(f"size      : {ratio(text, tokens)}")
        print()

    # A wider window reaches further back and needs fewer tokens.
    text = "the cat sat on the mat, the cat sat on the mat"
    for window in (8, 32, 64):
        print(f"window {window:>2}: {len(compress(text, window, 12))} tokens")


if __name__ == "__main__":
    main()
