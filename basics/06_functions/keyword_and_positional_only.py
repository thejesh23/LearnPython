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


def main() -> None:
    keyword_only_demo()


if __name__ == "__main__":
    main()
