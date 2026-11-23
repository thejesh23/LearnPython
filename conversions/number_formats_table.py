"""One number in many notations, using only format specifications.

Python's format mini-language already knows the common bases: "b" for binary,
"o" for octal, "x" and "X" for hex, with "#" adding the 0b / 0o / 0x prefix and
a width with a leading 0 padding to a fixed number of digits. "_" and ","
group digits for readability. The table below puts decimal, binary, octal,
hex and Roman side by side for a feel of how each base grows.

Negative numbers show the catch: format(-5, "b") is "-101", a sign plus a
magnitude. The bit pattern a CPU stores is two's complement, which needs a
fixed width; masking with (1 << bits) - 1 produces it.
"""

ROMAN: list[tuple[int, str]] = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def to_roman(n: int) -> str:
    out: list[str] = []
    for value, symbol in ROMAN:
        count, n = divmod(n, value)
        out.append(symbol * count)
    return "".join(out)


def twos_complement(n: int, bits: int) -> str:
    if not -(1 << (bits - 1)) <= n < (1 << (bits - 1)):
        raise ValueError(f"{n} does not fit in {bits} signed bits")
    return format(n & ((1 << bits) - 1), f"0{bits}b")


def main() -> None:
    header = f"{'dec':>5} {'bin':>12} {'oct':>5} {'hex':>4} {'roman':>10}"
    print(header)
    print("-" * len(header))
    for n in [1, 2, 3, 4, 7, 8, 10, 15, 16, 42, 64, 100, 255, 1000]:
        print(f"{n:>5} {n:>12b} {n:>5o} {n:>4X} {to_roman(n):>10}")

    n = 48879
    print(f"\nprefixes:  {n:#b}  {n:#o}  {n:#x}")
    print(f"padded:    {5:08b}  {5:04x}")
    print(f"grouped:   {2**32:_b}  {2**32:,}  {2**32:_x}")

    print("\nnegatives:")
    for v in [-1, -5, -128]:
        print(f"  {v:>5}: format gives {v:b}, 8-bit two's complement "
              f"{twos_complement(v, 8)}")

    back = all(int(format(v, "b"), 2) == v and int(format(v, "x"), 16) == v
               for v in range(-1000, 1000))
    print(f"\nint(format(v, base), base) == v for -1000..999: {back}")


if __name__ == "__main__":
    main()
