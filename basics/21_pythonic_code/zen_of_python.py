"""The Zen of Python — `import this`, and what a few of its lines mean in code.

PEP 20 is nineteen short aphorisms by Tim Peters about how Python code should
feel. It ships inside Python as an easter egg: `import this` prints it. When
people call code "Pythonic", these lines are most of what they mean.

The module prints the poem as a side effect of being imported, and only the
first time. To use the text as data we capture that print with
`contextlib.redirect_stdout`, which temporarily points `sys.stdout` at a
StringIO buffer.

The aphorisms are guidance, not law: the poem itself says "practicality
beats purity". Each demo below shows one line as a before/after pair.
"""

import io
from contextlib import redirect_stdout


def read_zen() -> list[str]:
    buffer = io.StringIO()
    with redirect_stdout(buffer):  # anything printed in here goes to buffer
        import this  # noqa: F401  (imported only for its printed side effect)
    return [line for line in buffer.getvalue().splitlines() if line]


ZEN = read_zen()


def zen_line(start: str) -> str:
    """The aphorism that begins with `start`."""
    return next(line for line in ZEN if line.startswith(start))


def capture_demo() -> None:
    title, *aphorisms = ZEN
    print(f"{title} -- {len(aphorisms)} aphorisms, the first five:")
    for line in aphorisms[:5]:
        print(f"  {line}")
    # A second import is a no-op: modules run only once per process.
    again = io.StringIO()
    with redirect_stdout(again):
        import this  # noqa: F401,F811
    print(f"printed again on second import: {bool(again.getvalue())}")


def shipping_nested(order: dict[str, object]) -> str:
    if order.get("paid"):
        if order.get("items"):
            if order.get("address"):
                return "ship it"
            else:
                return "no address"
        else:
            return "empty order"
    else:
        return "not paid"


def shipping_flat(order: dict[str, object]) -> str:
    # Guard clauses: deal with each problem and leave early. The happy path
    # ends up at the bottom, at the left margin, not four levels deep.
    if not order.get("paid"):
        return "not paid"
    if not order.get("items"):
        return "empty order"
    if not order.get("address"):
        return "no address"
    return "ship it"


def flat_demo() -> None:
    print(zen_line("Flat"))
    orders = [
        {"paid": True, "items": ["book"], "address": "1 Main St"},
        {"paid": True, "items": []},
        {"paid": False},
    ]
    for order in orders:
        nested, flat = shipping_nested(order), shipping_flat(order)
        print(f"  {flat:<12} same answer: {nested == flat}")


def parse_port_silent(text: str) -> int:
    try:
        return int(text)
    except Exception:  # swallows everything, even bugs, and hides the cause
        return 0


def parse_port_loud(text: str) -> int:
    port = int(text)  # let a ValueError for "abc" reach the caller
    if not 0 < port < 65536:
        raise ValueError(f"port out of range: {port}")
    return port


def errors_demo() -> None:
    print(zen_line("Errors should"))
    print(zen_line("Unless"))
    for text in ("8080", "abc", "70000"):
        silent = parse_port_silent(text)
        try:
            loud: object = parse_port_loud(text)
        except ValueError as exc:
            loud = f"ValueError: {exc}"
        print(f"  {text!r:>8}: silent -> {silent!r:<6} loud -> {loud}")
    # "Explicitly silenced" is fine: catch the ONE error you expect, on
    # purpose, and say what happens instead.
    fallback = 8080
    try:
        port = parse_port_loud("")
    except ValueError:
        port = fallback  # deliberate: an empty setting means "use the default"
    print(f"  empty setting falls back to {port}")


def no_guessing_demo() -> None:
    print(zen_line("In the face"))
    # Some languages guess that "3" + 4 means 7 or "34". Python refuses,
    # because either guess is wrong half the time.
    try:
        "3" + 4  # type: ignore[operator]
    except TypeError as exc:
        print(f"  '3' + 4 -> TypeError: {exc}")
    # You state the meaning you want, and the code says it too.
    print(f"  int('3') + 4 = {int('3') + 4}")
    print(f"  '3' + str(4) = {'3' + str(4)}")

    print(zen_line("Explicit"))
    # Bytes and text are not mixed up silently either: name the encoding.
    data = "café".encode("utf-8")
    print(f"  {data!r} decoded as utf-8 = {data.decode('utf-8')!r}")


def main() -> None:
    capture_demo()
    print()
    flat_demo()
    print()
    errors_demo()
    print()
    no_guessing_demo()


if __name__ == "__main__":
    main()
