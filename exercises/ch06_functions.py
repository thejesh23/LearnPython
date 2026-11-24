"""Practice exercises for basics/06_functions: parameters, closures, decorators.

How to work through them:
  1. Read the next exercise's docstring. It says what the function must
     return and gives examples.
  2. Replace its `raise NotImplementedError` line with your own code.
  3. Run this file:  python3 exercises/ch06_functions.py
  4. Read the report. Each exercise prints one line:
       [solved]       every check passed
       [not yet] ...  a check failed; the message shows the input, what
                      your function returned, and what was expected
       [todo]         not attempted yet
Aim for every line to say [solved]. The exercises get harder as you go
down. Under each one is a test_ function showing exactly what is checked:
read it when a message puzzles you, but leave it unchanged.

In this chapter the signature is part of the exercise: two of the stubs
below start with parameters that are incomplete or wrong, and fixing them
is the point. Nothing here needs more than basics/00 to basics/06 cover.

Worked solutions, with a note on each approach, are in
exercises/solutions/ch06_functions.py. Try each exercise yourself first.
"""

from collections.abc import Callable
from typing import Any


def verdict(error: BaseException) -> str:
    """Turn the exception a test raised into a short status."""
    # A stub raises NotImplementedError. Other errors may wrap it, so follow
    # the chain of causes (and look inside exception groups) before deciding.
    link: BaseException | None = error
    for _ in range(20):
        if link is None:
            break
        if isinstance(link, NotImplementedError):
            return "[todo] not attempted"
        if isinstance(link, BaseExceptionGroup) and link.subgroup(
            NotImplementedError
        ):
            return "[todo] not attempted"
        link = link.__cause__ or link.__context__
    if isinstance(error, AssertionError):
        return f"[not yet] {str(error) or 'a check failed'}"
    return f"[not yet] {type(error).__name__}: {error}"


def report(title: str, test: Callable[[Any], None], impl: Any) -> None:
    """Run one test against one implementation and print a one-line status."""
    try:
        test(impl)
        status = "[solved]"
    except KeyboardInterrupt:
        raise
    except BaseException as error:  # never crash: one line per exercise
        status = verdict(error)
    print(f"{title:<40} {status}")


def average(*numbers: float) -> float:
    """Return the mean of any number of arguments, or 0.0 when given none.

    average(1, 2, 3) -> 2.0
    average(5)       -> 5.0
    average()        -> 0.0
    """
    raise NotImplementedError


def test_average(fn: Callable[..., Any]) -> None:
    cases = [((1, 2, 3), 2.0), ((5,), 5.0), ((), 0.0), ((1, 2), 1.5), ((-4, 4), 0.0)]
    for args, want in cases:
        got = fn(*args)
        assert got == want, f"average{args} returned {got!r}, expected {want!r}"


def check_average() -> None:
    report("1. average", test_average, average)


def make_greeting(name: str) -> str:
    """Build a greeting such as "Hello, Ada!".

    Add two parameters to the signature (part of the exercise):
      greeting     second positional parameter, default "Hello"
      punctuation  keyword-only, default "!"

    make_greeting("Ada")                  -> "Hello, Ada!"
    make_greeting("Ada", "Hi")            -> "Hi, Ada!"
    make_greeting("Ada", punctuation="?") -> "Hello, Ada?"
    make_greeting("Ada", "Hi", "?")       -> TypeError (must be named)
    """
    raise NotImplementedError


def test_make_greeting(fn: Callable[..., Any]) -> None:
    calls = [
        (("Ada",), {}, "Hello, Ada!"),
        (("Ada", "Hi"), {}, "Hi, Ada!"),
        (("Ada",), {"greeting": "Welcome"}, "Welcome, Ada!"),
        (("Ada",), {"punctuation": "?"}, "Hello, Ada?"),
        (("Grace", "Hey"), {"punctuation": "."}, "Hey, Grace."),
    ]
    for args, kwargs, want in calls:
        got = fn(*args, **kwargs)
        assert got == want, (
            f"make_greeting with args {args} and keywords {kwargs} returned "
            f"{got!r}, expected {want!r}"
        )
    try:
        fn("Ada", "Hi", "?")
    except TypeError:
        pass
    else:
        raise AssertionError(
            'make_greeting("Ada", "Hi", "?") worked, but punctuation should be '
            "keyword-only; add a bare * before it in the signature"
        )


def check_make_greeting() -> None:
    report("2. make_greeting", test_make_greeting, make_greeting)


def append_to(item: int, items: list[int] = []) -> list[int]:
    """Append item to items and return the list.

    When a list is passed in, append to that very list and return it. When
    none is passed, start a brand-new empty list on every call.

    The default above is the shared-list trap from default_arguments.py:
    fix the signature as well as writing the body.

    append_to(1)       -> [1]
    append_to(2)       -> [2]     not [1, 2]
    append_to(8, [7])  -> [7, 8]
    """
    raise NotImplementedError


def test_append_to(fn: Callable[..., Any]) -> None:
    first = fn(1)
    assert first == [1], f"append_to(1) returned {first!r}, expected [1]"
    second = fn(2)
    assert second == [2], (
        f"a second call append_to(2) returned {second!r}, expected [2]: "
        "is one default list being shared between calls?"
    )
    mine = [7]
    result = fn(8, mine)
    assert mine == [7, 8] and result is mine, (
        f"append_to(8, mine) with mine = [7] left mine as {mine!r} and "
        f"returned {result!r}; expected it to append to mine and return it"
    )


def check_append_to() -> None:
    report("3. append_to", test_append_to, append_to)


def by_last_name(names: list[str]) -> list[str]:
    """Return a new list of full names sorted by their last word.

    Names sharing a last name keep their original order, and the list you
    are given must not change.

    by_last_name(["Ada Lovelace", "Alan Turing", "Grace Hopper"])
        -> ["Grace Hopper", "Ada Lovelace", "Alan Turing"]

    Hint: sorted() takes a key function, and a lambda is a quick one.
    """
    raise NotImplementedError


def test_by_last_name(fn: Callable[..., Any]) -> None:
    cases = [
        (["Ada Lovelace", "Alan Turing", "Grace Hopper"],
         ["Grace Hopper", "Ada Lovelace", "Alan Turing"]),
        (["Bo Smith", "Al Smith", "Cy Adams"], ["Cy Adams", "Bo Smith", "Al Smith"]),
        (["Guido van Rossum", "Tim Peters"], ["Tim Peters", "Guido van Rossum"]),
        ([], []),
    ]
    for names, want in cases:
        before = list(names)
        got = fn(names)
        assert got == want, (
            f"by_last_name({before!r}) returned {got!r}, expected {want!r}"
        )
        assert names == before, f"by_last_name changed its input list to {names!r}"


def check_by_last_name() -> None:
    report("4. by_last_name", test_by_last_name, by_last_name)


def main() -> None:
    check_average()
    check_make_greeting()
    check_append_to()
    check_by_last_name()


if __name__ == "__main__":
    main()
