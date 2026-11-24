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

import textwrap


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


SAMPLE = (
    "Python's standard library is often described as batteries included: "
    "it ships with modules for files, dates, text, networking and much more, "
    "so many small programs need nothing beyond a fresh install."
)


def textwrap_demo() -> None:
    # wrap() returns a list of lines no wider than width.
    lines = textwrap.wrap(SAMPLE, width=40)
    print(f"wrap -> {len(lines)} lines, longest {max(map(len, lines))} chars")

    # fill() is wrap() joined with newlines: ready to print.
    print("fill(width=40):")
    print(textwrap.fill(SAMPLE, width=40))

    # shorten() collapses whitespace and cuts at a word boundary.
    print(f"shorten: {textwrap.shorten(SAMPLE, width=50, placeholder=' [...]')}")

    # indent() prefixes every line, handy for nesting output.
    print("indent:")
    print(textwrap.indent(textwrap.fill(SAMPLE, width=36), "  | "))

    # dedent() removes the common leading spaces from an indented block.
    block = """
        name: demo
        tags:
          - text
    """
    print("dedent:")
    print(textwrap.dedent(block).strip())


def main() -> None:
    building_strings_demo()
    print()
    textwrap_demo()


if __name__ == "__main__":
    main()
