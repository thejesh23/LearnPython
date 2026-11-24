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


def main() -> None:
    capture_demo()


if __name__ == "__main__":
    main()
