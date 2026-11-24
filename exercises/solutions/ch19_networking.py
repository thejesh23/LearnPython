"""Solutions: networking (chapter 19).

Worked answers for exercises/ch19_networking.py. Try each exercise yourself
before reading its solution; the struggle is where the learning happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch19_networking.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import runpy
from pathlib import Path
from urllib.parse import parse_qs
from urllib.parse import parse_qsl
from urllib.parse import urlencode
from urllib.parse import urlsplit
from urllib.parse import urlunsplit


# Run the exercise file as a module (its main() does not run) to reuse its
# report() helper and test_... functions.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch19_networking.py")
)
report = EXERCISES["report"]


def get_param(url: str, name: str) -> str | None:
    # parse_qs decodes %XX and "+" and maps each name to a LIST of values.
    # Without keep_blank_values=True, "q=" would vanish instead of giving "".
    values = parse_qs(urlsplit(url).query, keep_blank_values=True).get(name)
    return values[0] if values else None


def check_get_param() -> None:
    report("1. get_param", EXERCISES["test_get_param"], get_param)


def add_params(url: str, params: dict[str, str | int]) -> str:
    parts = urlsplit(url)
    # A dict keeps insertion order, and updating an existing key keeps its
    # place, which is exactly the ordering the task asks for.
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update({name: str(value) for name, value in params.items()})
    return urlunsplit(parts._replace(query=urlencode(query)))


def check_add_params() -> None:
    report("2. add_params", EXERCISES["test_add_params"], add_params)


def main() -> None:
    check_get_param()
    check_add_params()


if __name__ == "__main__":
    main()
