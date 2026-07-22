"""LZW: build a dictionary of repeated strings while compressing, and never send it.

The encoder starts with a table holding every single character. It reads the
longest string w already in the table, emits w's code, then adds w + next_char
as a new entry. So the table grows by exactly one entry per emitted code.

The decoder can rebuild that same table because it is always one step behind:
after decoding a code it knows w, and the *next* code tells it the character
that followed, which is precisely the entry the encoder added. That lag causes
one edge case, the KwKwK pattern: if the incoming code is the entry the encoder
has just created but the decoder has not, the answer is provably previous +
previous[0], because such an entry can only arise that way.

Encoding is O(n) with a dict; the win comes from long repeated substrings.
"""


def encode(text: str) -> list[int]:
    table: dict[str, int] = {chr(i): i for i in range(256)}
    next_code = 256
    out: list[int] = []
    w = ""
    for ch in text:
        wc = w + ch
        if wc in table:
            w = wc
        else:
            out.append(table[w])
            table[wc] = next_code  # the entry the decoder will infer one step later
            next_code += 1
            w = ch
    if w:
        out.append(table[w])
    return out


def decode(codes: list[int]) -> str:
    if not codes:
        return ""
    table: dict[int, str] = {i: chr(i) for i in range(256)}
    next_code = 256
    prev = table[codes[0]]
    out = [prev]
    for code in codes[1:]:
        if code in table:
            entry = table[code]
        elif code == next_code:
            entry = prev + prev[0]  # KwKwK: the entry the encoder made this step
        else:
            raise ValueError(f"bad LZW code {code}")
        out.append(entry)
        table[next_code] = prev + entry[0]
        next_code += 1
        prev = entry
    return "".join(out)


def ratio(text: str, codes: list[int]) -> str:
    """Honest accounting: 12-bit codes against 8-bit input characters."""
    if not text:
        return "n/a (empty input)"
    before = len(text) * 8
    after = len(codes) * 12
    return f"{before} bits -> {after} bits ({after / before:.2f}x)"


def main() -> None:
    samples = [
        "",
        "TOBEORNOTTOBEORTOBEORNOT",
        "ababababababababababab",  # triggers the KwKwK case
        "no repeats here!",
    ]
    for text in samples:
        codes = encode(text)
        back = decode(codes)
        print(f"input     : {text!r}")
        print(f"codes     : {codes}")
        print(f"round-trip: {back == text}")
        print(f"size      : {ratio(text, codes)}")
        print()

    # Show the KwKwK branch firing explicitly.
    codes = encode("aaaaaa")
    print(f"'aaaaaa' -> {codes}; code 256 is used the moment it is created")
    print(f"decoded  -> {decode(codes)!r}")


if __name__ == "__main__":
    main()
