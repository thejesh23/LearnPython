"""Integers as Roman numerals, English words and digits in any base 2..36."""

ROMAN: list[tuple[int, str]] = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
    (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]
ROMAN_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"
ONES = ("zero one two three four five six seven eight nine ten eleven twelve "
        "thirteen fourteen fifteen sixteen seventeen eighteen nineteen").split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
SCALES = ["", "thousand", "million", "billion", "trillion", "quadrillion"]


def to_roman(n: int) -> str:
    """1..3999 to a canonical Roman numeral."""
    if not 1 <= n <= 3999:
        raise ValueError(f"{n} is outside 1..3999")
    out = []
    for value, symbol in ROMAN:
        count, n = divmod(n, value)
        out.append(symbol * count)
    return "".join(out)


def from_roman(text: str) -> int:
    """Parse a Roman numeral; rejects non-canonical spellings such as IIII."""
    if not text or any(ch not in ROMAN_VALUES for ch in text):
        raise ValueError(f"not a roman numeral: {text!r}")
    total = 0
    for here, after in zip(text, text[1:] + " "):
        value = ROMAN_VALUES[here]
        smaller = after != " " and value < ROMAN_VALUES[after]
        total += -value if smaller else value
    if not 1 <= total <= 3999 or to_roman(total) != text:
        raise ValueError(f"non-canonical numeral: {text!r}")
    return total


def _below_thousand(n: int) -> str:
    if n < 20:
        return ONES[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        return TENS[tens] + (f"-{ONES[ones]}" if ones else "")
    hundreds, rest = divmod(n, 100)
    head = f"{ONES[hundreds]} hundred"
    return f"{head} and {_below_thousand(rest)}" if rest else head


def to_words(n: int) -> str:
    """British-style English words: 1001 -> 'one thousand and one'."""
    if n == 0:
        return "zero"
    if n < 0:
        return "minus " + to_words(-n)
    groups: list[int] = []
    while n:
        n, group = divmod(n, 1000)
        groups.append(group)
    if len(groups) > len(SCALES):
        raise ValueError("number too large to name")
    named = [f"{_below_thousand(g)} {SCALES[i]}".rstrip()
             for i, g in reversed(list(enumerate(groups))) if g]
    if len(named) > 1 and 0 < groups[0] < 100:
        return ", ".join(named[:-1]) + " and " + named[-1]
    return ", ".join(named)


def to_base(n: int, base: int) -> str:
    """Digits of n in base 2..36, with a leading '-' for negatives."""
    if not 2 <= base <= 36:
        raise ValueError(f"base must be 2..36, not {base}")
    if n == 0:
        return "0"
    sign, n = ("-", -n) if n < 0 else ("", n)
    digits = []
    while n:
        n, d = divmod(n, base)
        digits.append(DIGITS[d])
    return sign + "".join(reversed(digits))


def from_base(text: str, base: int) -> int:
    """Inverse of to_base, by Horner's method."""
    sign, text = (-1, text[1:]) if text.startswith("-") else (1, text)
    value = 0
    for ch in text.lower():
        digit = DIGITS.find(ch)
        if not 0 <= digit < base:
            raise ValueError(f"{ch!r} is not a base-{base} digit")
        value = value * base + digit
    return sign * value
