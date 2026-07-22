"""Converting integers between bases by hand, without int() or bin().

A positional numeral is just a polynomial: the digits d_k ... d_0 in base b
mean d_k * b**k + ... + d_1 * b + d_0. Both directions fall straight out of
that. To write a number in base b, take n % b for the last digit, replace n
with n // b, and repeat: each step peels off the lowest digit. The digits come
out backwards, so reverse at the end.

To read a string in base b, run Horner's method: start at 0 and for each digit
do value = value * b + digit. That evaluates the polynomial left to right with
one multiply and one add per digit, and never builds a power of b explicitly.

Both directions are O(number of digits), which is O(log n) in the value. The
only fiddly parts are zero, which produces no digits at all and must be
special-cased, and negatives, where the sign is handled separately from the
magnitude.
"""

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def to_base(n: int, base: int) -> str:
    """Render n in the given base, 2 to 36, as a string."""
    if not 2 <= base <= 36:
        raise ValueError("base must be between 2 and 36")
    if n == 0:
        return "0"  # the loop below would produce an empty string
    negative = n < 0
    n = abs(n)
    out: list[str] = []
    while n:
        out.append(DIGITS[n % base])
        n //= base
    if negative:
        out.append("-")
    return "".join(reversed(out))


def from_base(text: str, base: int) -> int:
    """Parse a string in the given base back to an int, via Horner's method."""
    if not 2 <= base <= 36:
        raise ValueError("base must be between 2 and 36")
    text = text.strip().lower()
    if not text:
        raise ValueError("empty string is not a number")
    sign = 1
    if text[0] in "+-":
        sign = -1 if text[0] == "-" else 1
        text = text[1:]
    if not text:
        raise ValueError("a sign alone is not a number")
    value = 0
    for ch in text:
        digit = DIGITS.find(ch)
        if digit < 0 or digit >= base:
            raise ValueError(f"{ch!r} is not a digit in base {base}")
        value = value * base + digit
    return sign * value


def convert(text: str, from_b: int, to_b: int) -> str:
    """Rebase a string by going through an int in the middle."""
    return to_base(from_base(text, from_b), to_b)


def main() -> None:
    print(f"to_base(255, 2)  = {to_base(255, 2)}   (bin: {bin(255)})")
    print(f"to_base(255, 16) = {to_base(255, 16)}      (hex: {hex(255)})")
    print(f"to_base(255, 8)  = {to_base(255, 8)}      (oct: {oct(255)})")
    print(f"to_base(255, 36) = {to_base(255, 36)}")

    print(f"from_base('11111111', 2) = {from_base('11111111', 2)}")
    print(f"from_base('ff', 16)      = {from_base('ff', 16)}")
    print(f"from_base('-1010', 2)    = {from_base('-1010', 2)}")

    print(f"convert('deadbeef', 16, 2) = {convert('deadbeef', 16, 2)}")

    # Edge cases: zero, negatives, and a value far beyond 64 bits.
    print(f"to_base(0, 7)   = {to_base(0, 7)}")
    print(f"to_base(-42, 2) = {to_base(-42, 2)}")
    big = 2**200 + 12345
    print(f"round trip on 2**200 + 12345: "
          f"{from_base(to_base(big, 36), 36) == big}")

    try:
        from_base("129", 8)
    except ValueError as exc:
        print(f"rejected bad digit: {exc}")

    ok = all(from_base(to_base(n, b), b) == n
             for n in range(-200, 200) for b in range(2, 37))
    print(f"round trip holds for -200..199 in every base: {ok}")


if __name__ == "__main__":
    main()
