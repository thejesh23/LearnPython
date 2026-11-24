"""Solutions: the operating system and the command line (chapter 17).

Worked answers for exercises/ch17_os_and_command_line.py. Try each exercise
yourself before reading its solution; the struggle is where the learning
happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch17_os_and_command_line.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import argparse
import runpy
from collections.abc import Mapping
from pathlib import Path


# Run the exercise file as a module (its main() does not run) to reuse its
# report() helper and test_... functions.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch17_os_and_command_line.py")
)
report = EXERCISES["report"]


def env_settings(environ: Mapping[str, str], prefix: str) -> dict[str, str]:
    # removeprefix (3.9+) is safer than slicing by hand: no off-by-one.
    return {
        name.removeprefix(prefix).lower(): value
        for name, value in environ.items()
        if name.startswith(prefix)
    }


def check_env_settings() -> None:
    report("1. env_settings", EXERCISES["test_env_settings"], env_settings)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="resize", description="Resize an image.")
    parser.add_argument("image", help="the picture to resize")
    # type=int converts the string; a value like "wide" becomes an error.
    parser.add_argument("--width", type=int, default=800)
    parser.add_argument("--quality", choices=["low", "medium", "high"],
                        default="medium")
    # The dash becomes an underscore: args.dry_run.
    parser.add_argument("--dry-run", action="store_true")
    return parser


def check_build_parser() -> None:
    report("2. build_parser", EXERCISES["test_build_parser"], build_parser)


def main() -> None:
    check_env_settings()
    check_build_parser()


if __name__ == "__main__":
    main()
