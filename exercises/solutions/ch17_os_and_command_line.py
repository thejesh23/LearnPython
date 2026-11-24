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
import os
import runpy
import subprocess
import sys
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


def find_files(root: Path, suffix: str, skip: set[str]) -> list[str]:
    found = []
    for folder, dirs, files in os.walk(root):
        # Slice assignment changes the list os.walk is using, so it never
        # descends into the skipped folders at all.
        dirs[:] = [name for name in dirs if name not in skip]
        for name in files:
            if name.endswith(suffix):
                found.append((Path(folder) / name).relative_to(root).as_posix())
    return sorted(found)


def check_find_files() -> None:
    report("3. find_files", EXERCISES["test_find_files"], find_files)


def run_python(code: str) -> tuple[int, str, str]:
    # A list of arguments goes to the program as-is: no shell, so ; | >
    # are just characters. check=False (the default) keeps non-zero codes.
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, timeout=10
    )
    return result.returncode, result.stdout, result.stderr


def check_run_python() -> None:
    report("4. run_python", EXERCISES["test_run_python"], run_python)


def main() -> None:
    check_env_settings()
    check_build_parser()
    check_find_files()
    check_run_python()


if __name__ == "__main__":
    main()
