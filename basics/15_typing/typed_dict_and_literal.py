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
from typing import NotRequired
from typing import Required
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


class User(TypedDict):
    id: int
    name: str
    email: NotRequired[str]  # may be absent; when present it is a str


class SearchOptions(TypedDict, total=False):
    # total=False flips the default: every key is optional...
    query: Required[str]  # ...except the ones marked Required
    limit: int
    sort: str


def contact_line(user: User) -> str:
    # NotRequired means "the key may be missing", so use .get() or "in".
    # The checker warns about user["email"] because it can raise KeyError.
    email = user.get("email", "no email")
    return f"#{user['id']} {user['name']} <{email}>"


def optional_keys_demo() -> None:
    print(contact_line({"id": 1, "name": "Ana", "email": "ana@example.com"}))
    print(contact_line({"id": 2, "name": "Bo"}))

    # The required / optional split is recorded on the class.
    print(f"User required: {sorted(User.__required_keys__)}")
    print(f"User optional: {sorted(User.__optional_keys__)}")
    print(f"SearchOptions required: {sorted(SearchOptions.__required_keys__)}")
    print(f"SearchOptions optional: {sorted(SearchOptions.__optional_keys__)}")


def main() -> None:
    typed_dict_demo()
    print()
    optional_keys_demo()


if __name__ == "__main__":
    main()
