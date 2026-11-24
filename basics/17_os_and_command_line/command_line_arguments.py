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

import argparse
import contextlib
import io
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


def build_wordcount_parser() -> argparse.ArgumentParser:
    # prog= fixes the name shown in help; by default it is taken from sys.argv[0].
    parser = argparse.ArgumentParser(
        prog="wordcount",
        description="Count the most common words in a text file.",
    )
    parser.add_argument("file", help="the text file to read")
    parser.add_argument("-n", "--top", type=int, default=10,
                        help="how many words to show (default: %(default)s)")
    parser.add_argument("--order", choices=["count", "alpha"], default="count",
                        help="sort by count or alphabetically")
    return parser


def positional_and_optional_demo() -> None:
    parser = build_wordcount_parser()

    args = parser.parse_args(["notes.txt"])
    print(f"defaults: file={args.file!r} top={args.top} order={args.order!r}")

    # Short and long spellings set the same attribute, args.top.
    args = parser.parse_args(["notes.txt", "-n", "3", "--order", "alpha"])
    print(f"given:    file={args.file!r} top={args.top} order={args.order!r}")
    print(f"type=int converted it: {type(args.top).__name__}")

    # The --name=value spelling works too, and options may come first.
    args = parser.parse_args(["--top=5", "notes.txt"])
    print(f"--top=5 first: top={args.top}")


def build_flag_parser() -> argparse.ArgumentParser:
    parser = build_wordcount_parser()
    # store_true: absent means False, present means True. No value follows it.
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print progress messages")
    parser.add_argument("--ignore-case", action="store_true",
                        help="treat 'The' and 'the' as the same word")
    return parser


def flags_and_errors_demo() -> None:
    parser = build_flag_parser()
    args = parser.parse_args(["notes.txt", "-v", "--ignore-case"])
    # A dash in an option name becomes an underscore in the attribute name.
    print(f"verbose={args.verbose} ignore_case={args.ignore_case}")
    print(f"all parsed values: {vars(args)}")

    # format_help() returns the text that --help would print.
    print("\nwhat `wordcount --help` shows:")
    print(parser.format_help())

    # On bad input argparse prints a message to stderr and exits with code 2.
    # That exit is a SystemExit exception, so a test can catch it.
    for bad in (["notes.txt", "--top", "many"], ["notes.txt", "--order", "size"], []):
        captured = io.StringIO()
        try:
            with contextlib.redirect_stderr(captured):
                parser.parse_args(bad)
        except SystemExit as exc:
            last_line = captured.getvalue().strip().splitlines()[-1]
            print(f"{bad} -> exit code {exc.code}")
            print(f"    {last_line}")


def cmd_add(args: argparse.Namespace) -> str:
    return f"adding {args.name!r} with priority {args.priority}"


def cmd_done(args: argparse.Namespace) -> str:
    return f"marking task #{args.task_id} as done"


def build_todo_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo", description="A tiny to-do list.")
    subcommands = parser.add_subparsers(dest="command", required=True)

    # Each subcommand gets its own little parser with its own arguments.
    add = subcommands.add_parser("add", help="add a task")
    add.add_argument("name")
    add.add_argument("--priority", type=int, choices=[1, 2, 3], default=2)
    # set_defaults attaches the function that should handle this subcommand.
    add.set_defaults(handler=cmd_add)

    done = subcommands.add_parser("done", help="finish a task")
    done.add_argument("task_id", type=int)
    done.set_defaults(handler=cmd_done)
    return parser


def subcommands_demo() -> None:
    parser = build_todo_parser()
    for argv in (["add", "buy milk"], ["add", "fix bike", "--priority", "1"],
                 ["done", "4"]):
        args = parser.parse_args(argv)
        print(f"todo {' '.join(argv):<28} -> {args.handler(args)}")

    print("\nthe top-level help lists the subcommands:")
    print(parser.format_help())


def main() -> None:
    sys_argv_demo()
    print()
    positional_and_optional_demo()
    print()
    flags_and_errors_demo()
    print()
    subcommands_demo()


if __name__ == "__main__":
    main()
