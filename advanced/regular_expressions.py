"""`re` — patterns, groups, and the traps.

Always write patterns as raw strings (`r"\\d+"`) so backslashes reach the regex
engine intact. Compile a pattern you use in a loop; `re.compile` caches, but
the module-level functions still re-look-up the cache each call.

Two failure modes to recognise:
  - Greedy `.*` swallows too much; use `.*?` or a negated class `[^"]*`.
  - Catastrophic backtracking: nested quantifiers like `(a+)+b` against
    "aaaaaaaaaaaaaaaaaaaac" take exponential time. Avoid ambiguous nesting.
"""

import re


def main() -> None:
    text = "Ada was born 1815-12-10, Alan 1912-06-23."

    # search / match / fullmatch differ in where they anchor.
    print(f"search  -> {re.search(r'\d{4}', text).group()}")
    print(f"match   -> {re.match(r'\d{4}', text)}  (anchored at the start)")
    print(f"fullmatch('1815', r'\\d+') -> {re.fullmatch(r'\d+', '1815')}")

    # Groups: numbered, named, and non-capturing.
    date = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})")
    m = date.search(text)
    print(f"groups  -> {m.groups()}, named -> {m.groupdict()}, span -> {m.span()}")

    print(f"findall -> {date.findall(text)}")
    print(f"finditer spans -> {[mm.span() for mm in date.finditer(text)]}")

    # Substitution, with a function or a backreference.
    print(f"sub     -> {date.sub(r'\g<day>/\g<month>/\g<year>', text)}")
    print(f"sub fn  -> {re.sub(r'\d+', lambda mm: str(int(mm.group()) + 1), 'a1 b9')}")

    # split keeps the delimiters when they are captured.
    print(f"split   -> {re.split(r'[,.]\s*', text)}")
    print(f"split kept -> {re.split(r'(\d{4})', 'x1815y1912z')}")

    # Greedy vs lazy.
    html = '<a href="one">first</a><a href="two">second</a>'
    print(f"greedy  -> {re.findall(r'<a.*>', html)}")
    print(f"lazy    -> {re.findall(r'<a.*?>', html)}")
    print(f"negated -> {re.findall(r'href=\"([^\"]*)\"', html)}")

    # Flags: verbose patterns are the readable way to write anything complex.
    pattern = re.compile(
        r"""
        (?P<user>[\w.+-]+)   # local part
        @
        (?P<host>[\w-]+      # domain
        (?:\.[\w-]+)+)       # one or more labels
        """,
        re.VERBOSE,
    )
    print(f"email   -> {pattern.search('write to ada@example.co.uk').groupdict()}")
    print(f"IGNORECASE -> {re.findall(r'ada', 'ADA Ada aDa', re.IGNORECASE)}")

    # Lookahead / lookbehind match without consuming.
    print(f"lookahead  -> {re.findall(r'\d+(?= USD)', '30 USD, 40 EUR')}")
    print(f"lookbehind -> {re.findall(r'(?<=\$)\d+', 'costs $42 not 7')}")

    print("avoid nested quantifiers like (a+)+b — exponential backtracking")


if __name__ == "__main__":
    main()
