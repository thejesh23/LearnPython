"""Run-length encoding: replace each run of repeats with (count, character).

The simplest compression there is, and the honest lesson is that it *expands*
data without long runs — "abcd" becomes "1a1b1c1d". Real formats (PCX, TIFF,
fax) use a marker or a length byte so incompressible stretches cost only one
extra byte per block.

Encode and decode are exact inverses: `decode(encode(s)) == s` for any input.
"""

from itertools import groupby


def encode(text: str) -> list[tuple[int, str]]:
    return [(len(list(group)), ch) for ch, group in groupby(text)]


def decode(runs: list[tuple[int, str]]) -> str:
    return "".join(ch * count for count, ch in runs)


def encode_str(text: str) -> str:
    """Textual form: 'aaabb' -> 'a3b2'. Only shorter when runs are long."""
    return "".join(f"{ch}{count}" for count, ch in encode(text))


def decode_str(encoded: str) -> str:
    out: list[str] = []
    i = 0
    while i < len(encoded):
        ch = encoded[i]
        i += 1
        digits = ""
        while i < len(encoded) and encoded[i].isdigit():
            digits += encoded[i]
            i += 1
        out.append(ch * int(digits))
    return "".join(out)


def main() -> None:
    sample = "aaabbbccccd"
    runs = encode(sample)
    print(f"encode -> {runs}")
    print(f"decode -> {decode(runs)!r}, round-trip ok: {decode(runs) == sample}")

    print(f"encode_str -> {encode_str(sample)!r}")
    print(f"decode_str -> {decode_str(encode_str(sample))!r}")

    poor = "abcd"
    print(f"{poor!r} -> {encode_str(poor)!r}  (expanded: RLE is not universal)")
    print(f"empty round-trip: {decode(encode(''))!r}")


if __name__ == "__main__":
    main()
