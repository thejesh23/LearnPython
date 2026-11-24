r"""`re` — regular expressions for finding and rewriting text patterns.

A regular expression is a tiny pattern language:

    \d   a digit            \w   a word character    \s   whitespace
    .    any character      +    one or more         *    zero or more
    ?    optional           {3}  exactly three       [aeiou]  one of these
    ^ $  start / end        ( )  capture a group     |    either side

Always write patterns as raw strings (r"\d+"), so Python leaves the
backslashes alone for `re` to read. For simple jobs, string methods such as
`in`, `startswith` and `split` are clearer; reach for `re` when the shape of
the text matters.
"""

import re


def matching_demo() -> None:
    text = "Order 66 shipped on 2024-03-15"
    # search finds the first match anywhere in the string.
    found = re.search(r"\d+", text)
    print(f"search: {found.group() if found else None}")

    # match only tries at the very start; fullmatch must cover everything.
    digits = r"\d+"
    print(f"match at start: {re.match(digits, text)}")
    postcode = r"[A-Z]{2}\d{2}"
    for candidate in ["AB12", "AB123"]:
        print(f"fullmatch {candidate!r}: {bool(re.fullmatch(postcode, candidate))}")


def main() -> None:
    matching_demo()


if __name__ == "__main__":
    main()
