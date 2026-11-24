"""Practice: type hints (chapter 15).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch15_typing.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch15_typing.py: try first, peek second. The lessons
for this chapter are in basics/15_typing/.
"""

from collections.abc import Callable
from typing import Any
from typing import Literal
from typing import TypedDict
from typing import get_overloads


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


# Type hints do nothing at runtime by themselves, but they are stored on the
# function or class. The tests below read them back (__type_params__,
# __annotations__) to check that you wrote the hints the exercise asks for.

# --- Exercise 1 -------------------------------------------------------------

def first(items: list[Any], default: Any) -> Any:
    """Return the first item of the list, or default when the list is empty.

    Then replace the three Any hints with a type parameter, using the 3.12
    syntax, so a type checker knows the result has the items' type:
        def first[T](items: list[T], default: T) -> T:

    >>> first([3, 1, 2], 0), first([], "none")
    (3, 'none')
    """
    raise NotImplementedError


def test_first(impl: Callable[..., Any]) -> None:
    assert impl([3, 1, 2], 0) == 3, "first([3, 1, 2], 0) should be 3"
    assert impl([], "none") == "none", "an empty list should give the default"
    assert impl([None], 5) is None, "a None item is still the first item"
    params = getattr(impl, "__type_params__", ())
    assert len(params) == 1, "declare one type parameter: def first[T](...)"
    T = params[0]
    hints = impl.__annotations__
    assert hints.get("items") == list[T], "items should be hinted list[T]"
    assert hints.get("default") is T, "default should be hinted T"
    assert hints.get("return") is T, "the return type should be T"


def check_first() -> None:
    report("1. first[T]", test_first, first)


# --- Exercise 2 -------------------------------------------------------------

# Given: a type alias (3.12 `type` statement) naming the only valid modes.
type Mode = Literal["r", "w", "a"]


def parse_mode(text: str) -> Mode:
    """Return text unchanged if it is a valid Mode, else raise ValueError.

    Do not copy "r", "w", "a" into this function: read them from the alias,
    so adding a mode to Mode updates the check too. Mode.__value__ is the
    Literal[...] behind the alias, and typing.get_args() returns its values.
    The error message should include the bad text, e.g.
        ValueError: mode must be one of ('r', 'w', 'a'), got 'x'
    """
    raise NotImplementedError


def test_parse_mode(impl: Callable[[str], Any]) -> None:
    for mode in ("r", "w", "a"):
        got = impl(mode)
        assert got == mode, f"parse_mode({mode!r}) should return {mode!r}, got {got!r}"
    for bad in ("x", "R", "", "rw"):
        try:
            impl(bad)
        except ValueError as exc:
            assert repr(bad) in str(exc), f"the message should show {bad!r}: {exc}"
        else:
            raise AssertionError(f"parse_mode({bad!r}) should raise ValueError")


def check_parse_mode() -> None:
    report("2. parse_mode", test_parse_mode, parse_mode)


# --- Exercise 3 -------------------------------------------------------------

def double(value: int | str) -> int | str:
    """Double a number, or repeat a string twice.

    The hint `int | str -> int | str` loses information: double(2) is
    always an int and double("ab") always a str. Add two @typing.overload
    signatures directly above this function (bodies are just ...):
        @overload
        def double(value: int) -> int: ...
    and the same for str. The real function stays as it is below them.

    >>> double(21), double("ab")
    (42, 'abab')
    """
    raise NotImplementedError


def test_double(impl: Callable[[Any], Any]) -> None:
    assert impl(21) == 42, "double(21) should be 42"
    assert impl("ab") == "abab", "double('ab') should be 'abab'"
    assert impl(0) == 0 and impl("") == "", "zero and '' stay as they are"
    signatures = [o.__annotations__ for o in get_overloads(impl)]
    expected = [{"value": int, "return": int}, {"value": str, "return": str}]
    assert len(signatures) == 2, (
        f"add two @overload signatures above double, found {len(signatures)}"
    )
    for wanted in expected:
        assert wanted in signatures, f"missing an overload with hints {wanted}"


def check_double() -> None:
    report("3. double with @overload", test_double, double)


# --- Exercise 4 -------------------------------------------------------------

def compose(
    f: Callable[[Any], Any], g: Callable[[Any], Any]
) -> Callable[[Any], Any]:
    """Return a new function that computes g(f(x)).

    Then make the hints precise with three type parameters: f turns an A
    into a B, g turns a B into a C, so the result turns an A into a C:
        def compose[A, B, C](
            f: Callable[[A], B], g: Callable[[B], C]
        ) -> Callable[[A], C]:

    >>> length_doubled = compose(len, lambda n: n * 2)
    >>> length_doubled("abc")
    6
    """
    raise NotImplementedError


def test_compose(impl: Callable[..., Any]) -> None:
    length_doubled = impl(len, lambda n: n * 2)
    assert callable(length_doubled), "compose should return a function"
    assert length_doubled("abc") == 6, "compose(len, n * 2)('abc') should be 6"
    shout = impl(str.strip, str.upper)
    assert shout("  hi ") == "HI", f"strip then upper gave {shout('  hi ')!r}"
    calls: list[str] = []

    def record(x: int) -> int:
        calls.append("f")
        return x

    impl(record, str)
    assert calls == [], "compose should not call f until the new function runs"
    params = getattr(impl, "__type_params__", ())
    assert len(params) == 3, "declare three type parameters: def compose[A, B, C]"


def check_compose() -> None:
    report("4. compose[A, B, C]", test_compose, compose)


# --- Exercise 5 -------------------------------------------------------------

class Registry:
    """Named items of one type, e.g. a Registry[int] of settings.

    - register(name, item) stores the item; a name used twice raises
      ValueError.
    - get(name) returns the item; an unknown name raises KeyError(name).
    - names() returns the registered names, sorted.
    Then make the class generic with the 3.12 syntax, `class Registry[T]:`,
    and replace the Any hints below with T.

    >>> ports = Registry[int]()
    >>> ports.register("http", 80)
    >>> ports.get("http"), ports.names()
    (80, ['http'])
    """

    def __init__(self) -> None:
        raise NotImplementedError

    def register(self, name: str, item: Any) -> None:
        raise NotImplementedError

    def get(self, name: str) -> Any:
        raise NotImplementedError

    def names(self) -> list[str]:
        raise NotImplementedError


def test_registry(impl: type) -> None:
    ports = impl()
    ports.register("https", 443)
    ports.register("http", 80)
    assert ports.get("http") == 80, "get('http') should return 80"
    assert ports.names() == ["http", "https"], f"names() gave {ports.names()}"
    try:
        ports.register("http", 8080)
    except ValueError:
        pass
    else:
        raise AssertionError("registering a name twice should raise ValueError")
    try:
        ports.get("ftp")
    except KeyError:
        pass
    else:
        raise AssertionError("get() of an unknown name should raise KeyError")
    assert impl().names() == [], "each registry starts empty"
    params = getattr(impl, "__type_params__", ())
    assert len(params) == 1, "make it generic: class Registry[T]:"
    T = params[0]
    assert impl.get.__annotations__.get("return") is T, "get() should return T"
    assert impl[str]().names() == [], "Registry[str]() should work too"


def check_registry() -> None:
    report("5. Registry[T]", test_registry, Registry)


# --- Exercise 6 -------------------------------------------------------------

def type_errors(data: dict[str, object], schema: type) -> list[str]:
    """List the ways `data` does not match a TypedDict class `schema`.

    A TypedDict is only a hint; nothing checks real data at runtime. Write
    that check: typing.get_type_hints(schema) gives {field: type} in field
    order. Every field type is a plain class such as str, int or float.
    For each field, in order:
        missing from data         "missing: title"
        isinstance fails          "year: expected int, got str"
    then for each key of data that is not a field, in data order:
                                  "unexpected: color"
    Valid data gives [].
    """
    raise NotImplementedError


class Movie(TypedDict):
    """Given: a schema to check against."""

    title: str
    year: int
    rating: float


def test_type_errors(impl: Callable[[dict[str, object], type], list[str]]) -> None:
    good = {"title": "Up", "year": 2009, "rating": 8.3}
    assert impl(good, Movie) == [], f"valid data gave {impl(good, Movie)}"
    got = impl({"title": "Up", "year": "2009"}, Movie)
    expected = ["year: expected int, got str", "missing: rating"]
    assert got == expected, f"expected {expected}, got {got}"
    got = impl({**good, "color": "red", "3d": True}, Movie)
    expected = ["unexpected: color", "unexpected: 3d"]
    assert got == expected, f"expected {expected}, got {got}"

    class Point(TypedDict):
        x: int
        y: int

    got = impl({}, Point)
    assert got == ["missing: x", "missing: y"], f"an empty dict gave {got}"


def check_type_errors() -> None:
    report("6. type_errors", test_type_errors, type_errors)


def main() -> None:
    check_first()
    check_parse_mode()
    check_double()
    check_compose()
    check_registry()
    check_type_errors()


if __name__ == "__main__":
    main()
