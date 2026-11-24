"""Tools for building and reshaping text: join, textwrap, translate and string.

Strings are immutable, so "adding to" a string really makes a new one. For a
few pieces that is fine. For many pieces, collect them in a list and call
`"".join(parts)` once at the end; it is the standard Python idiom.

The rest of this file is a tour of small tools that save you from writing
fiddly loops:

    textwrap         wrap, fill, shorten and indent paragraphs of text
    str.translate    replace or delete many single characters in one pass
    string           ready-made character sets such as string.ascii_letters
    string.Template  simple $name substitution, safe for user-written templates
"""


def render_receipt(items: dict[str, float]) -> str:
    """Build a multi-line string by collecting lines, then joining them."""
    lines = ["RECEIPT"]
    for name, price in items.items():
        lines.append(f"{name:<10}{price:>8.2f}")
    lines.append(f"{'total':<10}{sum(items.values()):>8.2f}")
    return "\n".join(lines)


def building_strings_demo() -> None:
    # += works, but each step copies everything built so far. With thousands
    # of pieces that copying adds up; a list and one join does not.
    slow = ""
    for word in ["build", "it", "up"]:
        slow += word + " "
    print(f"with +=:  {slow.strip()!r}")
    print(f"with join: {' '.join(['build', 'it', 'up'])!r}")

    print(render_receipt({"coffee": 3.5, "bagel": 2.25, "juice": 4.0}))

    # join only accepts strings, so convert numbers first.
    numbers = [3, 1, 4, 1, 5]
    print(", ".join(str(n) for n in numbers))


def main() -> None:
    building_strings_demo()


if __name__ == "__main__":
    main()
