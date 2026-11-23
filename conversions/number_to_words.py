"""Integers to English words, built from three-digit groups.

Everything below 1000 comes from two small tables: the irregular names below
twenty, and the tens (twenty, thirty, ...). Larger numbers split into groups
of three digits from the right, and each non-zero group is spelled on its own
and given its scale word: 1_234_567 is "one million", "two hundred and
thirty-four thousand", "five hundred and sixty-seven". Zero groups are skipped,
which is why 1_000_001 has no "thousand" in it. A last group under a hundred
is joined with "and" in British style: "one thousand and one".

The British "and" after hundreds is a style choice; the flag turns it off for
the American form. Work is proportional to the number of digits.
"""

ONES = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
        "eighty", "ninety"]
SCALES = ["", "thousand", "million", "billion", "trillion", "quadrillion"]


def below_thousand(n: int, use_and: bool = True) -> str:
    if n < 20:
        return ONES[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        return TENS[tens] + (f"-{ONES[ones]}" if ones else "")
    hundreds, rest = divmod(n, 100)
    head = f"{ONES[hundreds]} hundred"
    if not rest:
        return head
    return f"{head} {'and ' if use_and else ''}{below_thousand(rest, use_and)}"


def to_words(n: int, use_and: bool = True) -> str:
    if n == 0:
        return "zero"
    if n < 0:
        return "minus " + to_words(-n, use_and)
    groups: list[int] = []
    while n:
        n, group = divmod(n, 1000)
        groups.append(group)
    if len(groups) > len(SCALES):
        raise ValueError("number too large to name")
    named = [f"{below_thousand(g, use_and)} {SCALES[i]}".rstrip()
             for i, g in reversed(list(enumerate(groups))) if g]
    # British style joins a trailing group under 100 with "and":
    # "one thousand and one", not "one thousand, one".
    if use_and and len(named) > 1 and 0 < groups[0] < 100:
        return ", ".join(named[:-1]) + " and " + named[-1]
    return ", ".join(named)


def main() -> None:
    for n in [0, 7, 13, 19, 20, 42, 100, 101, 305, 999, 1000, 1001, 1234,
              1_000_000, 1_000_001, 2_147_483_647, -52]:
        print(f"{n:>14,}: {to_words(n)}")

    print(f"\nAmerican style 1234: {to_words(1234, use_and=False)}")

    # Words are a fun stress test: which number below 1000 has the longest name?
    longest = max(range(1000), key=lambda n: len(to_words(n)))
    print(f"longest name below 1000: {longest} ({to_words(longest)})")

    try:
        to_words(10**18)
    except ValueError as err:
        print(f"10**18: {err}")


if __name__ == "__main__":
    main()
