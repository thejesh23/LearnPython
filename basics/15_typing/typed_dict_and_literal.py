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
from typing import Any
from typing import Literal
from typing import NotRequired
from typing import Required
from typing import TypedDict
from typing import get_args
from typing import get_origin
from typing import get_type_hints


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


Status = Literal["todo", "doing", "done"]  # an alias keeps it in one place


def next_status(status: Status) -> Status:
    # The checker rejects next_status("finished"): it is not one of the three.
    # Unlike an Enum there is nothing to import; callers pass plain strings.
    order: list[Status] = ["todo", "doing", "done"]
    return order[min(order.index(status) + 1, len(order) - 1)]


def read_file(path: str, mode: Literal["r", "rb"] = "r") -> str:
    # Literal shines for "mode" or "kind" flags that take a few exact strings.
    return f"would open {path!r} with mode {mode!r}"


def literal_demo() -> None:
    print(f"next_status('todo') = {next_status('todo')!r}")
    print(f"next_status('done') = {next_status('done')!r}")
    print(read_file("notes.txt"))

    # get_args reads the allowed values back, handy for runtime checks.
    allowed = get_args(Status)
    print(f"allowed statuses: {allowed}")
    print(f"'finished' allowed: {'finished' in allowed}")


class Task(TypedDict):
    title: str
    status: Status


class Project(TypedDict):
    # TypedDicts nest, so a whole JSON document can be described this way.
    name: str
    owner: User
    tasks: list[Task]


def problems_with_task(data: dict[str, Any]) -> list[str]:
    """Check one task dict against the Task hints and report what is wrong."""
    problems = [f"missing key {key!r}" for key in sorted(Task.__required_keys__)
                if key not in data]
    for key, hint in get_type_hints(Task).items():
        if key not in data:
            continue
        value = data[key]
        if get_origin(hint) is Literal:  # Literal hints: compare values
            if value not in get_args(hint):
                problems.append(f"{key}={value!r} not in {get_args(hint)}")
        elif not isinstance(value, hint):  # plain classes such as str
            problems.append(f"{key} should be {hint.__name__}")
    return problems


def validate_demo() -> None:
    raw = """
    {"name": "launch", "owner": {"id": 7, "name": "Kai"},
     "tasks": [{"title": "write docs", "status": "doing"},
               {"title": "ship", "status": "finished"},
               {"status": "todo"}]}
    """
    project: Project = json.loads(raw)
    print(f"project {project['name']!r} owned by {contact_line(project['owner'])}")
    for task in project["tasks"]:
        found = problems_with_task(dict(task))
        label = task.get("title", "?")
        print(f"  {label:<11} {'ok' if not found else '; '.join(found)}")
    # For real projects, libraries such as pydantic do this checking for you.


def main() -> None:
    typed_dict_demo()
    print()
    optional_keys_demo()
    print()
    literal_demo()
    print()
    validate_demo()


if __name__ == "__main__":
    main()
