"""Reading command-line arguments: `sys.argv` by hand, then `argparse`.

When you run `python wordcount.py notes.txt --top 3`, Python puts the words of
that command into the list `sys.argv`. Item 0 is the script name; everything
after it is a plain string, exactly as typed. Turning those strings into
numbers, spotting flags and printing a helpful message on mistakes is tedious,
so the standard library ships `argparse` to do it:

    positional       required, identified by position     notes.txt
    optional         starts with - or --, has a default    --top 3
    flag             on/off, no value after it             --verbose
    type= choices=   convert and validate the string
    subcommands      the `git commit` / `git push` shape

`parser.parse_args()` reads `sys.argv` by default, but it also accepts a list.
This file passes lists, so it runs the same way without any real arguments,
and that is also how you test a command-line tool.
"""

import sys
from pathlib import Path


def parse_by_hand(argv: list[str]) -> dict[str, object]:
    """A tiny hand-written parser, to show what argparse saves you from."""
    options: dict[str, object] = {"file": None, "top": 10}
    i = 0
    while i < len(argv):
        if argv[i] == "--top":
            options["top"] = int(argv[i + 1])  # IndexError if the value is missing
            i += 2
        else:
            options["file"] = argv[i]
            i += 1
    return options


def sys_argv_demo() -> None:
    # sys.argv[0] is the script; the rest are the words after it on the command.
    print(f"script name: {Path(sys.argv[0]).name}")
    print(f"extra arguments given: {sys.argv[1:]}")

    # Pretend the user typed: python wordcount.py notes.txt --top 3
    fake_argv = ["notes.txt", "--top", "3"]
    print(f"by hand: {parse_by_hand(fake_argv)}")
    # Every value arrives as a string; the "3" only became 3 because we said so.
    try:
        parse_by_hand(["notes.txt", "--top"])
    except IndexError:
        print("by hand, '--top' with no value crashes with IndexError")


def main() -> None:
    sys_argv_demo()


if __name__ == "__main__":
    main()
