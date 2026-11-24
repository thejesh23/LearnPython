"""Worked solutions for exercises/ch04_strings.py.

Try each exercise yourself before reading its solution here: the struggle
is where the learning happens. Each solution has a short comment on the
approach. Yours does not have to match, as long as the tests pass.

Running this file checks every solution with the very same tests the
exercise file uses. They are loaded from that file rather than copied, so
the two can never disagree about what "correct" means. Every line should
say [solved].
"""

import runpy
from pathlib import Path


# Run the exercise file as a module and keep its globals: report() and the
# test_ functions come from there.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch04_strings.py")
)
report = EXERCISES["report"]


def format_price(amount: float) -> str:
    # `,` adds thousands separators and `.2f` rounds to two decimals; in a
    # format spec the comma goes before the precision.
    return f"${amount:,.2f}"


def check_format_price() -> None:
    report("1. format_price", EXERCISES["test_format_price"], format_price)


def initials(full_name: str) -> str:
    # split() with no argument drops leading, trailing and repeated spaces,
    # so the unpacking always sees exactly two words.
    first, last = full_name.split()
    return f"{first[0]}.{last[0]}.".upper()


def check_initials() -> None:
    report("2. initials", EXERCISES["test_initials"], initials)


def is_palindrome(text: str) -> bool:
    # Normalise first, then compare with the reversed copy s[::-1].
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]


def check_is_palindrome() -> None:
    report("3. is_palindrome", EXERCISES["test_is_palindrome"], is_palindrome)


def mask_card(number: str) -> str:
    # "*" * n is "" when n is zero or negative, and digits[-4:] is the whole
    # string when it is short, so short numbers need no special case.
    digits = number.replace(" ", "")
    return "*" * (len(digits) - 4) + digits[-4:]


def check_mask_card() -> None:
    report("4. mask_card", EXERCISES["test_mask_card"], mask_card)


def parse_setting(line: str) -> tuple[str, str]:
    # partition splits at the first "=" and always returns three parts,
    # with an empty value when there is no "=", so it never raises.
    key, _, value = line.partition("=")
    return key.strip(), value.strip()


def check_parse_setting() -> None:
    report("5. parse_setting", EXERCISES["test_parse_setting"], parse_setting)


def main() -> None:
    check_format_price()
    check_initials()
    check_is_palindrome()
    check_mask_card()
    check_parse_setting()


if __name__ == "__main__":
    main()
