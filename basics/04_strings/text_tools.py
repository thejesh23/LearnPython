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

import string
import textwrap
from string import Template


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


def translate_demo() -> None:
    # maketrans(from, to) pairs characters by position; translate applies
    # every swap in a single pass over the string.
    leet = str.maketrans("aeiost", "4310$7")
    print(f"leet speak: {'translate is fast'.translate(leet)}")

    # A third argument lists characters to delete.
    no_punct = str.maketrans("", "", ",.!?;:")
    print(f"punctuation removed: {'Hello, world! Ready?'.translate(no_punct)}")

    # A dict works too, and can map one character to a longer string.
    escapes = str.maketrans({"<": "&lt;", ">": "&gt;", "&": "&amp;"})
    print(f"escaped: {'a < b & b > c'.translate(escapes)}")

    # Compare with chained replace(): fine for two swaps, clumsy for ten,
    # and wrong when one swap's output feeds the next.
    swapped = "left right".replace("left", "right").replace("right", "left")
    print(f"chained replace: {swapped!r}   <- both became 'left'")
    lr = str.maketrans({"L": "R", "R": "L"})
    print(f"translate swaps safely: {'L R L'.translate(lr)!r}")


def is_valid_username(name: str) -> bool:
    """Letters, digits and underscore only, 3 to 12 characters."""
    allowed = set(string.ascii_letters + string.digits + "_")
    return 3 <= len(name) <= 12 and set(name) <= allowed


def string_constants_demo() -> None:
    print(f"ascii_lowercase = {string.ascii_lowercase}")
    print(f"ascii_uppercase = {string.ascii_uppercase}")
    print(f"digits          = {string.digits}")
    print(f"hexdigits       = {string.hexdigits}")
    print(f"punctuation     = {string.punctuation}")

    for name in ["ada_99", "no spaces", "x", "Grace"]:
        print(f"  {name!r:<12} valid? {is_valid_username(name)}")

    # capwords: split on spaces, capitalize each word, join again.
    print(f"capwords: {string.capwords('the quick  brown fox')}")


def template_demo() -> None:
    # $name placeholders, filled in from keyword arguments or a dict.
    greeting = Template("Hello $name, your order #$order ships ${day}day.")
    print(greeting.substitute(name="Ada", order=42, day="Mon"))

    # substitute() insists on every value; safe_substitute() leaves gaps.
    partial = Template("Dear $name, your code is $code.")
    try:
        partial.substitute(name="Alan")
    except KeyError as exc:
        print(f"KeyError: missing {exc}")
    print(partial.safe_substitute(name="Alan"))

    # Why use Template at all, when f-strings exist? A template can come from
    # a file or a user. It can only fill in names, never run code, unlike
    # str.format, whose fields can reach into attributes of what you pass.
    user_text = "Thanks, $who! ($$5 off next time)"
    print(Template(user_text).substitute(who="Grace"))


def main() -> None:
    building_strings_demo()
    print()
    textwrap_demo()
    print()
    translate_demo()
    print()
    string_constants_demo()
    print()
    template_demo()


if __name__ == "__main__":
    main()
