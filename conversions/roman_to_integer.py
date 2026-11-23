"""Roman numeral to integer, with validation.

Walk the symbols left to right and add each value, except when a symbol is
smaller than the one after it: then it is the first half of a subtractive pair
(IV, IX, XL, XC, CD, CM) and is subtracted instead. MCMXCIV reads as
1000 - 100 + 1000 - 10 + 100 - 1 + 5 = 1994. One pass, O(n) in the length.

That rule is lenient: it happily turns "IIII" into 4 and "IC" into 99, neither
of which is a standard numeral. The cheap strict check is to convert back and
compare, since every value in 1..3999 has exactly one canonical spelling.
"""

VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

TABLE: list[tuple[int, str]] = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def from_roman(s: str) -> int:
    if not s or any(ch not in VALUES for ch in s):
        raise ValueError(f"not a roman numeral: {s!r}")
    total = 0
    for here, after in zip(s, s[1:] + " "):
        value = VALUES[here]
        total += -value if after != " " and value < VALUES[after] else value
    return total


def to_roman(n: int) -> str:
    out: list[str] = []
    for value, symbol in TABLE:
        count, n = divmod(n, value)
        out.append(symbol * count)
    return "".join(out)


def from_roman_strict(s: str) -> int:
    n = from_roman(s)
    if not 1 <= n <= 3999 or to_roman(n) != s:
        raise ValueError(f"non-canonical numeral: {s!r}")
    return n


def main() -> None:
    for s in ["III", "IV", "IX", "LVIII", "MCMXCIV", "MMXXIV", "MMMCMXCIX"]:
        print(f"{s:>10} -> {from_roman(s)}")

    round_trip = all(from_roman(to_roman(n)) == n for n in range(1, 4000))
    print(f"\nround trip on 1..3999: {round_trip}")

    print("\nlenient vs strict:")
    for s in ["IIII", "IC", "VX", "MCMXCIV", "XM"]:
        try:
            strict = str(from_roman_strict(s))
        except ValueError:
            strict = "rejected"
        print(f"  {s:>8}: lenient {from_roman(s):>4}, strict {strict}")

    for bad in ["", "ABC", "xiv"]:
        try:
            from_roman(bad)
        except ValueError as err:
            print(f"rejected: {err}")


if __name__ == "__main__":
    main()
