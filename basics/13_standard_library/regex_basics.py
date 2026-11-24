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


def groups_demo() -> None:
    # Parentheses capture pieces of the match; (?P<name>...) names them.
    pattern = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
    m = re.search(pattern, "released on 2024-03-15, patched later")
    if m:
        print(f"whole match: {m.group(0)}")
        print(f"by position: {m.group(1)}, by name: {m['month']}")
        print(f"as a dict: {m.groupdict()}")


def find_all_demo() -> None:
    log = "user=ana id=17; user=bo id=4; user=cy id=230"
    # With no groups, findall returns the matched strings.
    numbers = re.findall(r"\d+", log)
    print(f"numbers: {numbers}")
    # With groups, it returns tuples of the groups.
    pairs = re.findall(r"user=(\w+) id=(\d+)", log)
    print(f"pairs: {pairs}")
    # finditer yields match objects, which also know their positions.
    for m in re.finditer(r"id=(\d+)", log):
        print(f"  id {m.group(1)} at columns {m.start()}-{m.end()}")


def substitute_demo() -> None:
    # sub replaces every match; \1 in the replacement refers to group 1.
    print(re.sub(r"(\w+)@(\w+)\.com", r"\1 at \2", "mail ana@example.com"))

    # The replacement can be a function that receives each match.
    prices = "apple 1.20, pear 0.80"
    doubled = re.sub(r"\d+\.\d+", lambda m: f"{float(m.group()) * 2:.2f}", prices)
    print(f"doubled: {doubled}")

    # Collapse runs of whitespace into a single space.
    print(re.sub(r"\s+", " ", "too    many\n\nspaces   here"))


EMAIL = re.compile(
    r"""
    ^[\w.+-]+      # the name part
    @
    [\w-]+          # domain
    (\.[\w-]+)+$    # one or more .suffix parts
    """,
    re.VERBOSE,
)


def compiled_demo() -> None:
    # re.compile builds the pattern once; VERBOSE allows spaces and comments.
    for address in ["ana@example.com", "bo.smith+news@mail.co.uk", "no-at-sign.com"]:
        print(f"{address:<26} valid: {bool(EMAIL.match(address))}")

    # IGNORECASE is one of several flags.
    found = re.findall(r"python", "Python PYTHON python", re.IGNORECASE)
    print(f"case-insensitive: {found}")


def main() -> None:
    matching_demo()
    print()
    groups_demo()
    print()
    find_all_demo()
    print()
    substitute_demo()
    print()
    compiled_demo()


if __name__ == "__main__":
    main()
