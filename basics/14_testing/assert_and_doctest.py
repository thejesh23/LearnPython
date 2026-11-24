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


def main() -> None:
    assert_demo()


if __name__ == "__main__":
    main()
