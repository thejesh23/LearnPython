"""Keyword-only (`*`) and positional-only (`/`) parameters.

By default a parameter can be passed either way: f(1, 2) or f(a=1, b=2). Two
markers in the parameter list narrow that down:

    def f(a, b, /, c, *, d): ...
          ^^^^  ^  ^  ^  ^
          |     |  |  |  d can only be given by name
          |     |  |  everything after * is keyword-only
          |     |  c can be given either way
          |     everything before / is positional-only
          a and b can only be given by position

Keyword-only arguments make call sites readable (no mystery `True` flags).
Positional-only ones let you rename a parameter later without breaking
callers, because no caller can have used its name.
"""


def connect(host: str, port: int, *, timeout: float = 5.0, retry: bool = False) -> str:
    return f"{host}:{port} timeout={timeout} retry={retry}"


def keyword_only_demo() -> None:
    # connect("db", 5432, 2.0, True) would be unreadable: which flag is True?
    # The * forces the options to be named at every call site.
    print(connect("db", 5432, timeout=2.0, retry=True))
    print(connect("db", 5432))
    try:
        connect("db", 5432, 2.0)  # type: ignore[misc]
    except TypeError as exc:
        print(f"TypeError: {exc}")


def distance(x1: float, y1: float, x2: float, y2: float, /) -> float:
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def positional_only_demo() -> None:
    print(f"distance = {distance(0, 0, 3, 4)}")
    try:
        distance(x1=0, y1=0, x2=3, y2=4)  # type: ignore[call-arg]
    except TypeError as exc:
        print(f"TypeError: {exc}")
    # Many built-ins already work this way: len(obj=[1]) is an error too.
    try:
        len(obj=[1, 2])  # type: ignore[call-arg]
    except TypeError as exc:
        print(f"built-in len: {exc}")


def main() -> None:
    keyword_only_demo()
    print()
    positional_only_demo()


if __name__ == "__main__":
    main()
