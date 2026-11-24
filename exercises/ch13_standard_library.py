"""Practice: the standard library (chapter 13).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch13_standard_library.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch13_standard_library.py: try first, peek second.
The lessons for this chapter are in basics/13_standard_library/.
"""

from collections.abc import Callable
from datetime import date
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


# --- Exercise 1 -------------------------------------------------------------

def top_words(text: str, n: int) -> list[tuple[str, int]]:
    """Return the n most common words in text with their counts.

    Split on whitespace, strip the punctuation .,!?;: from both ends of each
    word, lowercase it, and skip anything left empty. collections.Counter
    and its most_common(n) method do the rest (ties keep first-seen order).

    >>> top_words("The cat. The dog! the END", 2)
    [('the', 3), ('cat', 1)]
    """
    raise NotImplementedError


def test_top_words(impl: Callable[[str, int], list[tuple[str, int]]]) -> None:
    got = impl("The cat. The dog! the END", 2)
    assert got == [("the", 3), ("cat", 1)], f"got {got}"
    text = "a b a c b a d; ...  b? A!"
    got = impl(text, 3)
    assert got == [("a", 4), ("b", 3), ("c", 1)], f"for {text!r} got {got}"
    assert impl("", 5) == [], "empty text has no words"
    assert impl("hi hi", 10) == [("hi", 2)], "n larger than the vocabulary is fine"


def check_top_words() -> None:
    report("1. top_words", test_top_words, top_words)


# --- Exercise 2 -------------------------------------------------------------

def group_by_length(words: list[str]) -> dict[int, list[str]]:
    """Group words by their length, keeping the input order inside each group.

    collections.defaultdict(list) lets you append without checking whether
    the key exists yet.

    >>> group_by_length(["hi", "cat", "yo", "dog", "a"])
    {2: ['hi', 'yo'], 3: ['cat', 'dog'], 1: ['a']}
    """
    raise NotImplementedError


def test_group_by_length(impl: Callable[[list[str]], dict[int, list[str]]]) -> None:
    got = impl(["hi", "cat", "yo", "dog", "a"])
    expected = {2: ["hi", "yo"], 3: ["cat", "dog"], 1: ["a"]}
    assert got == expected, f"expected {expected}, got {got}"
    assert impl([]) == {}, "no words should give an empty dict"
    got = impl(["same", "same"])
    assert got == {4: ["same", "same"]}, f"duplicates are kept, got {got}"
    assert 99 not in got and len(got) == 1, "only lengths that occur are keys"


def check_group_by_length() -> None:
    report("2. group_by_length", test_group_by_length, group_by_length)


# --- Exercise 3 -------------------------------------------------------------

def moving_average(values: list[float], window: int) -> list[float]:
    """Average of each run of `window` consecutive values.

    A collections.deque(maxlen=window) drops its oldest item by itself when
    a new one is appended. Emit an average once the window is full. A window
    below 1 makes no sense: raise ValueError.

    >>> moving_average([1, 2, 3, 4, 5], 3)
    [2.0, 3.0, 4.0]
    """
    raise NotImplementedError


def test_moving_average(impl: Callable[[list[float], int], list[float]]) -> None:
    got = impl([1, 2, 3, 4, 5], 3)
    assert got == [2.0, 3.0, 4.0], f"window 3 over 1..5 gave {got}"
    got = impl([10, 20, 30], 1)
    assert got == [10.0, 20.0, 30.0], f"window 1 gives the values, got {got}"
    got = impl([4, 8], 2)
    assert got == [6.0], f"window 2 over [4, 8] gave {got}"
    assert impl([1, 2], 5) == [], "a window larger than the data gives []"
    try:
        impl([1, 2, 3], 0)
    except ValueError:
        pass
    else:
        raise AssertionError("window=0 should raise ValueError")


def check_moving_average() -> None:
    report("3. moving_average", test_moving_average, moving_average)


# --- Exercise 4 -------------------------------------------------------------

def add_business_days(start: date, days: int) -> date:
    """Return the date `days` working days after start, skipping weekends.

    Step one day at a time with timedelta(days=1) and only count Monday to
    Friday (date.weekday() is 0 for Monday, 5 and 6 for the weekend).
    days is never negative; adding 0 days returns start unchanged.

    >>> add_business_days(date(2026, 11, 20), 1)   # a Friday
    datetime.date(2026, 11, 23)
    """
    raise NotImplementedError


def test_add_business_days(impl: Callable[[date, int], date]) -> None:
    friday = date(2026, 11, 20)
    cases = [
        (friday, 0, friday),
        (friday, 1, date(2026, 11, 23)),
        (date(2026, 11, 16), 4, date(2026, 11, 20)),  # Monday + 4 = Friday
        (date(2026, 11, 21), 1, date(2026, 11, 23)),  # Saturday + 1 = Monday
        (friday, 10, date(2026, 12, 4)),
        (date(2026, 12, 30), 3, date(2027, 1, 4)),  # across a new year
    ]
    for start, days, expected in cases:
        got = impl(start, days)
        assert got == expected, (
            f"{start:%a %Y-%m-%d} + {days} business days should be "
            f"{expected:%a %Y-%m-%d}, got {got}"
        )


def check_add_business_days() -> None:
    report("4. add_business_days", test_add_business_days, add_business_days)


# --- Exercise 5 -------------------------------------------------------------

def us_to_iso(text: str) -> str:
    r"""Rewrite every MM/DD/YYYY date in text as YYYY-MM-DD.

    Only exact two-digit month and day and four-digit year count, standing
    as a whole word (use \b at both ends). Capture the parts with groups and
    put them back in a new order with re.sub; leave all other text alone.

    >>> us_to_iso("due 12/31/2026, paid 01/02/2027")
    'due 2026-12-31, paid 2027-01-02'
    """
    raise NotImplementedError


def test_us_to_iso(impl: Callable[[str], str]) -> None:
    cases = [
        ("due 12/31/2026, paid 01/02/2027", "due 2026-12-31, paid 2027-01-02"),
        ("no dates here", "no dates here"),
        ("short 1/2/2026 stays", "short 1/2/2026 stays"),
        ("too long 112/31/20267 stays", "too long 112/31/20267 stays"),
        ("(07/04/1776)", "(1776-07-04)"),
        ("", ""),
    ]
    for text, expected in cases:
        got = impl(text)
        assert got == expected, f"us_to_iso({text!r}) gave {got!r}, not {expected!r}"


def check_us_to_iso() -> None:
    report("5. us_to_iso", test_us_to_iso, us_to_iso)


# --- Exercise 6 -------------------------------------------------------------

def count_paths(rows: int, cols: int) -> int:
    """Count the routes across a grid, moving only right or down.

    Routes go from the top-left cell to the bottom-right cell.
    A grid with a single row or a single column has exactly 1 route. Any
    other grid's routes start either down or right, so:
        count_paths(rows, cols) = count_paths(rows - 1, cols)
                                + count_paths(rows, cols - 1)
    Written that way the same sub-grids are counted again and again. Put
    @functools.cache on the function so each answer is computed only once.

    >>> count_paths(3, 3)
    6
    """
    raise NotImplementedError


def test_count_paths(impl: Callable[[int, int], int]) -> None:
    cases = [((1, 1), 1), ((1, 5), 1), ((4, 1), 1), ((2, 2), 2), ((3, 3), 6),
             ((3, 7), 28)]
    for (rows, cols), expected in cases:
        got = impl(rows, cols)
        assert got == expected, (
            f"count_paths({rows}, {cols}) should be {expected}, got {got}"
        )
    assert hasattr(impl, "cache_info"), "decorate count_paths with @functools.cache"
    # Without the cache this call would take minutes; with it, microseconds.
    got = impl(18, 18)
    assert got == 2_333_606_220, f"count_paths(18, 18) gave {got}"


def check_count_paths() -> None:
    report("6. count_paths", test_count_paths, count_paths)


def main() -> None:
    check_top_words()
    check_group_by_length()
    check_moving_average()
    check_add_business_days()
    check_us_to_iso()
    check_count_paths()


if __name__ == "__main__":
    main()
