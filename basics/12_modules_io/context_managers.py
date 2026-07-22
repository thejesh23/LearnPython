"""`with` — guaranteed cleanup, even when something raises.

A context manager defines `__enter__` (setup, its return value is bound by
`as`) and `__exit__` (teardown, which runs no matter how the block ends). That
is why `with open(...)` is the only correct way to open a file: the handle is
closed on an exception, on a `return`, on anything.

`contextlib.contextmanager` turns a generator into one: everything before the
`yield` is setup, everything after is teardown, and a `try/finally` around the
yield makes the teardown exception-proof.
"""

import time
from contextlib import contextmanager, suppress


class Timer:
    def __init__(self, label: str) -> None:
        self.label = label

    def __enter__(self) -> "Timer":
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.elapsed = time.perf_counter() - self.start
        print(f"  {self.label} took {self.elapsed * 1000:.2f} ms")
        return False  # False = do not swallow the exception


@contextmanager
def temporary_setting(store: dict[str, str], key: str, value: str):
    original = store.get(key)
    store[key] = value
    try:
        yield store  # the body of the `with` runs here
    finally:  # runs even if the body raises
        if original is None:
            del store[key]
        else:
            store[key] = original


def main() -> None:
    with Timer("sum to a million"):
        total = sum(range(1_000_000))
    print(f"total = {total}")

    settings = {"mode": "prod"}
    with temporary_setting(settings, "mode", "debug") as s:
        print(f"inside:  {s}")
    print(f"outside: {settings}")

    # Teardown still happens when the block raises.
    with suppress(RuntimeError):
        with temporary_setting(settings, "mode", "debug"):
            raise RuntimeError("boom inside the block")
    print(f"after an exception: {settings}  (restored)")

    # Several managers in one statement; they exit in reverse order.
    with Timer("outer"), Timer("inner"):
        pass

    # contextlib.suppress is a readable `except X: pass`.
    with suppress(ZeroDivisionError):
        1 / 0
    print("ZeroDivisionError suppressed deliberately")


if __name__ == "__main__":
    main()
