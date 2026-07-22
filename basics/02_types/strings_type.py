"""`str` — an immutable sequence of Unicode characters.

Immutable means every "modification" returns a *new* string; the original is
untouched. That is why `s.upper()` must be assigned to something to matter.

A Python str holds code points, not bytes. Encoding to bytes is an explicit
step (`.encode()`), and decoding back is its mirror. Keeping those two worlds
separate is what makes Python 3 text handling predictable.
"""


def main() -> None:
    s = "Ada Lovelace"
    print(f"len = {len(s)}")
    print(f"upper = {s.upper()}   (original still: {s})")

    # Strings are sequences: index, slice, iterate.
    print(f"s[0] = {s[0]}   s[-1] = {s[-1]}   s[:3] = {s[:3]}")

    # ...but they cannot be mutated in place.
    try:
        s[0] = "B"  # type: ignore[index]
    except TypeError as exc:
        print(f"immutable: {exc}")

    # Unicode: one code point can still be more than one byte.
    text = "héllo ☃"
    print(f"code points = {len(text)}, utf-8 bytes = {len(text.encode('utf-8'))}")
    print(f"encoded = {text.encode('utf-8')!r}")
    print(f"round-trip = {text.encode('utf-8').decode('utf-8')}")

    # Adjacent literals concatenate at parse time — handy for long text.
    banner = "Learn" "Python"
    print(banner)

    # Building a string in a loop with += is O(n^2); join is the idiom.
    parts = ["a", "b", "c", "d"]
    print("-".join(parts))


if __name__ == "__main__":
    main()
