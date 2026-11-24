"""`TypedDict` and `Literal` — describing JSON-like data with types.

Data that arrives as JSON (an API response, a config file) becomes plain dicts,
lists, strings and numbers. Converting all of it to classes is often overkill,
but `dict[str, Any]` tells a reader nothing. Two tools fill the gap:

    TypedDict      a dict with a fixed set of keys, each with its own type
    Required /     mark single keys as must-be-present or may-be-missing
    NotRequired
    Literal        "one of these exact values", e.g. Literal["open", "closed"]

Both exist only for the type checker. At runtime a TypedDict *is* a dict and a
Literal hint is not checked, which is why the last part of this file shows how
to read the hints back and validate incoming data yourself.
"""

import json
from typing import TypedDict


class Movie(TypedDict):
    title: str
    year: int


def describe(movie: Movie) -> str:
    # The checker knows movie["year"] is an int and flags typos such as
    # movie["yaer"]. Without the TypedDict it would only know "some value".
    return f"{movie['title']} ({movie['year']})"


def typed_dict_demo() -> None:
    # Call it like a class, or write a dict literal; both give a plain dict.
    heat = Movie(title="Heat", year=1995)
    alien: Movie = {"title": "Alien", "year": 1979}
    print(describe(heat))
    print(describe(alien))
    print(f"type(heat) is dict: {type(heat) is dict}")

    # Parsed JSON fits straight in. json.loads returns Any, so annotate it.
    raw = '{"title": "Up", "year": 2009}'
    up: Movie = json.loads(raw)
    print(f"from JSON: {describe(up)}")
    print(f"Movie.__annotations__ = {Movie.__annotations__}")


def main() -> None:
    typed_dict_demo()


if __name__ == "__main__":
    main()
