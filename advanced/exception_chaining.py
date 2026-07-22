"""Traceback anatomy: `__cause__`, `__context__`, and reading a failure.

Every exception carries three attributes worth knowing:
    __context__     set automatically when one exception is raised inside the
                    handling of another ("During handling ... another occurred")
    __cause__       set explicitly by `raise X from Y` ("The above was the
                    direct cause")
    __traceback__   the frame chain, walkable with the traceback module

`raise X from Y` states intent — this failure is a translation of that one.
`raise X from None` suppresses the context, which is right when the inner
exception is an implementation detail the caller must not care about.
"""

import traceback


class ConfigError(Exception):
    pass


def load(raw: dict[str, str], key: str) -> int:
    try:
        return int(raw[key])
    except KeyError as exc:
        raise ConfigError(f"missing {key!r}") from exc  # explicit cause
    except ValueError:
        raise ConfigError(f"{key!r} is not a number") from None  # suppressed


def implicit_context() -> None:
    try:
        1 / 0
    except ZeroDivisionError:
        raise RuntimeError("cleanup also failed")  # __context__ set implicitly


def main() -> None:
    print("explicit cause (raise ... from exc):")
    try:
        load({}, "port")
    except ConfigError as exc:
        print(f"  {type(exc).__name__}: {exc}")
        print(f"  __cause__:   {exc.__cause__!r}")
        print(f"  __context__: {exc.__context__!r}")

    print("suppressed context (raise ... from None):")
    try:
        load({"port": "http"}, "port")
    except ConfigError as exc:
        print(f"  {exc} | cause={exc.__cause__} suppressed={exc.__suppress_context__}")

    print("implicit context:")
    try:
        implicit_context()
    except RuntimeError as exc:
        print(f"  {exc} | context={exc.__context__!r}")

    print("formatted traceback:")
    try:
        load({}, "host")
    except ConfigError as exc:
        lines = traceback.format_exception(type(exc), exc, exc.__traceback__)
        for line in "".join(lines).rstrip().splitlines():
            print(f"  {line}")

    print("walking the frames:")
    try:
        load({}, "host")
    except ConfigError as exc:
        for frame in traceback.extract_tb(exc.__traceback__):
            print(f"  {frame.name} at line {frame.lineno}: {frame.line}")

    print("exception groups keep several failures together:")
    try:
        raise ExceptionGroup("two problems", [ValueError("bad value"), KeyError("k")])
    except* ValueError as group:
        print(f"  ValueErrors: {[str(e) for e in group.exceptions]}")
    except* KeyError as group:
        print(f"  KeyErrors:   {[str(e) for e in group.exceptions]}")


if __name__ == "__main__":
    main()
