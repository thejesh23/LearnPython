"""A mini Markdown to HTML converter.

Markdown is the plain-text format behind README files: `# Title` becomes a
heading, `**bold**` becomes bold. You build a small converter for the most
used parts of it in two layers, the same way real converters are built:

    inline   rewrites text *inside* a line: emphasis, code spans, links.
             Regular expressions do this well.
    blocks   decides what each *line* belongs to: a heading, a paragraph, a
             list item, a code block. This needs memory of the previous lines
             (am I inside a list?), so it is a small state machine: an object
             with a `state` that each new line can change.

Each stage adds one feature by subclassing the previous converter, so you can
see exactly what each block type costs. It is deliberately not complete
Markdown (no nested lists, tables or block quotes); the stdlib has no Markdown
module, and for real work you would install one.

Uses:
    04_strings             startswith, strip, join, raw strings
    05_control_flow        if/elif chains, for loops over lines
    06_functions           small pure functions for each inline rule
    09_classes             a class with state, inheritance and super()
    13_standard_library    re (groups, sub, split), html.escape
"""

import html
import re


CODE_SPAN = re.compile(r"(`[^`]+`)")
BOLD = re.compile(r"\*\*(.+?)\*\*")
ITALIC = re.compile(r"\*(.+?)\*")
# [text](url) where the url has no spaces, quotes or closing parenthesis.
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s\"]+)\)")


def format_text(text: str) -> str:
    """Apply the inline rules to text that is not inside a code span."""
    # Escape first, so a literal <script> in the input is shown, not run.
    # Markdown's own symbols (* [ ] ( )) are untouched by escaping.
    text = html.escape(text, quote=False)
    text = LINK.sub(r'<a href="\2">\1</a>', text)
    # Bold before italic: otherwise ** would be read as two single stars.
    text = BOLD.sub(r"<strong>\1</strong>", text)
    text = ITALIC.sub(r"<em>\1</em>", text)
    return text


def inline(text: str) -> str:
    """Convert one line of inline Markdown to HTML."""
    # split() with a capturing group keeps the separators: the code spans
    # land at the odd indexes, ordinary text at the even ones.
    parts = CODE_SPAN.split(text)
    out: list[str] = []
    for i, part in enumerate(parts):
        if i % 2:
            # Inside `code`, stars and brackets are shown as typed.
            out.append(f"<code>{html.escape(part[1:-1], quote=False)}</code>")
        else:
            out.append(format_text(part))
    return "".join(out)


def inline_demo() -> None:
    print("== stage 1: inline rules ==")
    for source in [
        "plain words stay plain",
        "some **bold** and *italic* text",
        "call `print(*args)` here, stars kept",
        "see [the docs](https://docs.python.org/3/) for more",
        "a <b>tag</b> & an ampersand are escaped",
        "**[bold link](https://example.org)**",
    ]:
        print(f"  {source}")
        print(f"  -> {inline(source)}")


def main() -> None:
    inline_demo()


if __name__ == "__main__":
    main()
