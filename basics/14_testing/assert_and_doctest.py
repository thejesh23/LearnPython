"""The two lightest ways to check code: `assert` and doctest.

`assert condition, message` raises AssertionError when the condition is
false. It documents what you believe must be true at that point, and fails
loudly the moment it is not.

A doctest is an example session pasted into a docstring: each line that
starts with the >>> prompt is run, and its output must match the line below.
The examples are
documentation for readers *and* tests for the computer, so they cannot
quietly go out of date.
"""

import doctest
import textwrap


def average(values: list[float]) -> float:
    # An assert states an assumption the rest of the function relies on.
    assert values, "average() needs at least one value"
    return sum(values) / len(values)


def assert_demo() -> None:
    print(f"average([2, 4, 9]) = {average([2, 4, 9])}")
    try:
        average([])
    except AssertionError as exc:
        print(f"AssertionError: {exc}")

    # Running "python -O" strips every assert, so never use assert to check
    # user input or anything that must always be enforced; raise an
    # exception for those. Use assert for "this cannot happen" checks.
    print(f"asserts are active in this run: {__debug__}")


def slugify(title: str) -> str:
    """Turn a title into a URL-friendly slug.

    >>> slugify("Hello World")
    'hello-world'
    >>> slugify("  Python 3.12: What's New?  ")
    'python-312-whats-new'
    >>> slugify("")
    ''
    """
    kept = "".join(ch for ch in title.lower() if ch.isalnum() or ch == " ")
    return "-".join(kept.split())


def doctest_demo() -> None:
    # testmod finds every >>> example in this module and checks its output.
    # The same check runs from the shell with: python -m doctest -v file.py
    results = doctest.testmod()
    print(f"doctest: {results.attempted} examples, {results.failed} failed")

    # A wrong expectation shows up as a readable failure report.
    def broken() -> None:
        """
        >>> 1 + 1
        3
        """

    finder = doctest.DocTestFinder()
    runner = doctest.DocTestRunner(verbose=False)
    report: list[str] = []
    for test in finder.find(broken, "broken", globs={}):
        runner.run(test, out=report.append)
    failure = "".join(report).split("Failed example:")[1].strip()
    print("a failing example is reported like this:")
    print(textwrap.indent(failure, "  "))


def main() -> None:
    assert_demo()
    print()
    doctest_demo()


if __name__ == "__main__":
    main()
