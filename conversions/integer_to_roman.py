"""Integer to Roman numeral, for the classical range 1..3999.

The greedy rule is: subtract the largest value that still fits, write its
symbol, repeat. That alone would turn 900 into DCCCC, so the six subtractive
pairs (CM, CD, XC, XL, IX, IV) go into the table as first-class values. With
them in place, greedy is exactly right: each decimal digit is written
independently, and the table holds every symbol a single digit can need.

The loop runs at most fifteen times (3888 = MMMDCCCLXXXVIII is the longest
numeral), so the cost is O(1). Values outside 1..3999 have no standard form
and are rejected.
"""

TABLE: list[tuple[int, str]] = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def to_roman(n: int) -> str:
    if not 1 <= n <= 3999:
        raise ValueError(f"{n} is outside 1..3999")
    out: list[str] = []
    for value, symbol in TABLE:
        count, n = divmod(n, value)
        out.append(symbol * count)
    return "".join(out)


def to_roman_by_digit(n: int) -> str:
    """Same result, built one decimal digit at a time from lookup rows."""
    if not 1 <= n <= 3999:
        raise ValueError(f"{n} is outside 1..3999")
    thousands = ["", "M", "MM", "MMM"]
    hundreds = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    tens = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    ones = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
    return (thousands[n // 1000] + hundreds[n // 100 % 10]
            + tens[n // 10 % 10] + ones[n % 10])


def main() -> None:
    for n in [1, 4, 9, 14, 40, 90, 400, 1994, 2024, 3888, 3999]:
        print(f"{n:>4} -> {to_roman(n)}")

    agree = all(to_roman(n) == to_roman_by_digit(n) for n in range(1, 4000))
    print(f"\ngreedy and digit-table agree on 1..3999: {agree}")
    longest = max(range(1, 4000), key=lambda n: len(to_roman(n)))
    print(f"longest numeral: {longest} = {to_roman(longest)}")

    for bad in [0, 4000, -5]:
        try:
            to_roman(bad)
        except ValueError as err:
            print(f"rejected: {err}")


if __name__ == "__main__":
    main()
