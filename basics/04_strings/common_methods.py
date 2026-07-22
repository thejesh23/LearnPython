"""The string methods you will reach for daily.

Every one of these returns a *new* string — `str` is immutable, so nothing is
modified in place. Assign the result or it is lost.

`split` and `join` are inverses and belong together: split turns text into a
list, join turns a list back into text. Note that join is a method on the
*separator*, not on the list.
"""


def main() -> None:
    s = "  Hello, World!  "

    print(f"strip()      -> {s.strip()!r}")
    print(f"lstrip()     -> {s.lstrip()!r}")
    print(f"rstrip(' !') -> {s.rstrip(' !')!r}")

    t = s.strip()
    print(f"upper()      -> {t.upper()}")
    print(f"lower()      -> {t.lower()}")
    print(f"title()      -> {'hello world'.title()}")
    print(f"replace()    -> {t.replace('World', 'Python')}")

    print(f"startswith() -> {t.startswith('Hello')}")
    print(f"endswith()   -> {t.endswith('!')}")
    print(f"find('World')-> {t.find('World')}   find('x') -> {t.find('x')}  (-1, no raise)")
    print(f"count('l')   -> {t.count('l')}")

    # split / join are inverses.
    csv = "a,b,,c"
    print(f"split(',')   -> {csv.split(',')}")
    print(f"split()      -> {'  a  b   c '.split()}  (whitespace runs collapse)")
    print(f"','.join(...)-> {','.join(['a', 'b', 'c'])}")
    print(f"splitlines() -> {'one\\ntwo'.splitlines()}")

    # partition splits once and always returns three parts.
    print(f"partition('=')-> {'key=value=more'.partition('=')}")

    # Classification helpers, handy for validating input.
    for probe in ("42", "4.2", "abc", "abc123", ""):
        print(f"{probe!r:>8}: isdigit={probe.isdigit():<5} isalpha={probe.isalpha():<5} isalnum={probe.isalnum()}")

    # Padding and alignment without an f-string.
    print("center:", "menu".center(20, "-"))
    print("zfill: ", "42".zfill(6))


if __name__ == "__main__":
    main()
