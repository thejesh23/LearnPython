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


HEADING = re.compile(r"(#{1,6})\s+(.*)")


class BlockConverter:
    """Headings and paragraphs.

    `state` names the block that is open right now. A paragraph can span
    several lines, so its lines wait in `buffer` until something ends it: a
    blank line, a heading, or the end of the text.
    """

    def __init__(self) -> None:
        self.out: list[str] = []
        self.state = "idle"
        self.buffer: list[str] = []

    def convert(self, text: str) -> str:
        for line in text.splitlines():
            self.feed(line.rstrip())
        self.close_block()  # the last block has nothing after it to close it
        return "\n".join(self.out)

    def close_block(self) -> None:
        if self.state == "paragraph":
            self.out.append(f"<p>{inline(' '.join(self.buffer))}</p>")
        self.buffer = []
        self.state = "idle"

    def feed(self, line: str) -> None:
        if not line.strip():
            self.close_block()
        elif m := HEADING.match(line):
            self.close_block()
            level = len(m[1])
            self.out.append(f"<h{level}>{inline(m[2])}</h{level}>")
        else:
            if self.state != "paragraph":
                self.close_block()
                self.state = "paragraph"
            self.buffer.append(line.strip())


def show(source: str, converter: BlockConverter) -> None:
    print("markdown:")
    for line in source.strip("\n").splitlines():
        print(f"  | {line}".rstrip())
    print("html:")
    for line in converter.convert(source).splitlines():
        print(f"  | {line}")


def blocks_demo() -> None:
    print("== stage 2: headings and paragraphs ==")
    source = """
# Notes
A paragraph can be
spread over *three*
lines in the source.

## Second heading
Another paragraph.
"""
    show(source, BlockConverter())


BULLET = re.compile(r"[-*]\s+(.*)")
NUMBERED = re.compile(r"\d+\.\s+(.*)")


class ListConverter(BlockConverter):
    """Adds two states, "ul" and "ol", for bullet and numbered lists."""

    def close_block(self) -> None:
        if self.state in ("ul", "ol"):
            self.out.append(f"</{self.state}>")
        super().close_block()

    def feed(self, line: str) -> None:
        if m := BULLET.match(line):
            kind = "ul"
        elif m := NUMBERED.match(line):
            kind = "ol"
        else:
            # Not a list item: let the parent decide. Its close_block() call
            # still reaches ours, so an open list is closed properly.
            super().feed(line)
            return
        if self.state != kind:
            self.close_block()  # ends a paragraph, or a list of the other kind
            self.out.append(f"<{kind}>")
            self.state = kind
        self.out.append(f"  <li>{inline(m[1])}</li>")


def lists_demo() -> None:
    print("== stage 3: lists ==")
    source = """
Shopping:
- **eggs**
- milk
1. preheat the oven
2. mix
Done.
"""
    show(source, ListConverter())


class MarkdownConverter(ListConverter):
    """Adds fenced code blocks: lines between ``` markers are copied as-is."""

    def close_block(self) -> None:
        if self.state == "code":
            body = "\n".join(html.escape(line, quote=False) for line in self.buffer)
            self.out.append(f"<pre><code>{body}</code></pre>")
        super().close_block()

    def feed(self, line: str) -> None:
        if self.state == "code":
            # Inside a fence nothing is special except the closing fence:
            # no headings, no lists, no inline rules.
            if line.startswith("```"):
                self.close_block()
            else:
                self.buffer.append(line)
        elif line.startswith("```"):
            self.close_block()
            self.state = "code"
        else:
            super().feed(line)


def markdown_to_html(text: str) -> str:
    """Convert a whole document. A new converter each time: they hold state."""
    return MarkdownConverter().convert(text)


SAMPLE = """
# Project notes

This tool turns **Markdown** into *HTML*. See
[the guide](https://www.markdownguide.org/basic-syntax/).

## Install
1. Download it
2. Run `python convert.py notes.md`

## Example

```
# not a heading: code is copied as typed
if a < b and **kwargs:
    print("<ok>")
```

## Limits
- no tables
- no nested lists
"""


def full_document_demo() -> None:
    print("== stage 4: a whole document ==")
    show(SAMPLE, MarkdownConverter())
    html_text = markdown_to_html(SAMPLE)
    print(f"{len(html_text.splitlines())} lines of HTML, "
          f"{html_text.count('<h')} headings, {html_text.count('<li>')} list items")


def main() -> None:
    inline_demo()
    print()
    blocks_demo()
    print()
    lists_demo()
    print()
    full_document_demo()


if __name__ == "__main__":
    main()
