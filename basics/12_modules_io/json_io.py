"""JSON — `dumps`/`loads` for strings, `dump`/`load` for files.

The four names differ by one letter: the `s` suffix means "string". Everything
else is the same.

JSON's type system is smaller than Python's, so the round trip is lossy in
predictable ways: tuples come back as lists, dict keys become strings, and
sets, dates, and dataclasses are not representable at all until you supply a
`default=` function.

Never `eval()` JSON. `json.loads` is safe; `eval` executes whatever it is given.
"""

import json
from dataclasses import asdict, dataclass, is_dataclass
from datetime import date


@dataclass
class User:
    name: str
    joined: date
    tags: set[str]


def encode(obj: object) -> object:
    """Called by json for anything it cannot serialise itself."""
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, set):
        return sorted(obj)
    raise TypeError(f"cannot serialise {type(obj).__name__}")


def main() -> None:
    payload = {"name": "Ada", "age": 36, "tags": ["math", "code"], "active": True}

    text = json.dumps(payload)
    print(f"dumps -> {text}")
    print(f"indented:\n{json.dumps(payload, indent=2, sort_keys=True)}")

    back = json.loads(text)
    print(f"loads -> {back}, equal: {back == payload}")

    # Type mapping surprises.
    lossy = json.loads(json.dumps({"pair": (1, 2), 3: "int key", "none": None}))
    print(f"tuple became {type(lossy['pair']).__name__}, "
          f"int key became {list(lossy)[1]!r}, None became {lossy['none']!r}")

    # Custom types need a default= hook.
    user = User("Ada", date(1843, 1, 1), {"math", "code"})
    print(f"custom -> {json.dumps(user, default=encode)}")
    try:
        json.dumps(user)
    except TypeError as exc:
        print(f"without default=: {exc}")

    # Malformed input raises a subclass of ValueError, with position info.
    try:
        json.loads("{'single': 'quotes'}")
    except json.JSONDecodeError as exc:
        print(f"JSONDecodeError at line {exc.lineno} col {exc.colno}: {exc.msg}")

    # File form: json.dump / json.load, wrapped in `with`.
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "user.json"
        with path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        with path.open(encoding="utf-8") as fh:
            print(f"round-tripped from disk: {json.load(fh) == payload}")


if __name__ == "__main__":
    main()
