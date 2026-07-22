"""`argparse` — command-line interfaces with parsing, help, and validation free.

The pattern: build a parser, declare arguments, call `parse_args()`. You get
`--help` output, type conversion, defaults, and error messages with the correct
exit code without writing any of it.

Worth knowing: `type=` accepts any callable (including your own validator),
`action="store_true"` makes a flag, `nargs` collects several values, mutually
exclusive groups reject contradictory options, and subparsers give you the
`git commit` / `git push` shape.

`parse_args()` reads `sys.argv` by default, but accepts a list — which is how
you test a CLI without spawning a process, as `main()` does below.
"""

import argparse


def positive_int(raw: str) -> int:
    value = int(raw)
    if value <= 0:
        raise argparse.ArgumentTypeError(f"{raw} is not positive")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fetch",
        description="Fetch records from a source.",
        epilog="Example: fetch db --limit 10 --verbose",
    )
    parser.add_argument("source", help="where to read from")
    parser.add_argument("-l", "--limit", type=positive_int, default=100,
                        help="maximum records (default: %(default)s)")
    parser.add_argument("-o", "--output", default="-", help="output path, - for stdout")
    parser.add_argument("-v", "--verbose", action="store_true", help="chatty output")
    parser.add_argument("--tag", action="append", default=[], help="repeatable")
    parser.add_argument("--fields", nargs="+", metavar="FIELD", help="one or more fields")
    parser.add_argument("--format", choices=("json", "csv", "table"), default="json")

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--fast", action="store_true")
    mode.add_argument("--thorough", action="store_true")
    return parser


def build_subcommands() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tool")
    subs = parser.add_subparsers(dest="command", required=True)

    add = subs.add_parser("add", help="add an item")
    add.add_argument("name")
    add.add_argument("--count", type=int, default=1)

    remove = subs.add_parser("remove", help="remove an item")
    remove.add_argument("name")
    remove.add_argument("--force", action="store_true")
    return parser


def main() -> None:
    parser = build_parser()

    args = parser.parse_args(["db", "--limit", "10", "-v", "--tag", "a", "--tag", "b"])
    print(f"parsed: source={args.source} limit={args.limit} verbose={args.verbose} "
          f"tags={args.tag} format={args.format}")

    args = parser.parse_args(["api", "--fields", "id", "name", "email", "--format", "csv"])
    print(f"nargs='+': fields={args.fields}, format={args.format}")

    print("validation errors exit with code 2 and a message:")
    for bad in (["db", "--limit", "-5"], ["db", "--format", "xml"],
                ["db", "--fast", "--thorough"], []):
        try:
            parser.parse_args(bad)
        except SystemExit as exc:
            print(f"  {bad} -> SystemExit({exc.code})")

    print("subcommands:")
    sub = build_subcommands()
    for argv in (["add", "widget", "--count", "3"], ["remove", "widget", "--force"]):
        parsed = sub.parse_args(argv)
        print(f"  {argv} -> {vars(parsed)}")

    print("generated help:")
    for line in parser.format_help().splitlines()[:6]:
        print(f"  {line}")


if __name__ == "__main__":
    main()
