"""What happens to type hints when the program actually runs.

Short answer: almost nothing. Python stores the hints on the function or class
and then ignores them. A function hinted `(n: int) -> int` will accept a string
without complaint. The checking is done *before* running, by a separate tool:

    mypy file.py        (pip install mypy)
    pyright file.py     (pip install pyright, also built into VS Code's Pylance)

This file looks at the runtime side:
    __annotations__     the raw hints, possibly still strings
    get_type_hints()    the hints resolved into real objects
    TYPE_CHECKING       a flag that is False at runtime and True for checkers,
                        for imports only the checker needs
    a small decorator   that uses the hints to check arguments at runtime
"""


def double(n: int) -> int:
    return n * 2


def not_enforced_demo() -> None:
    print(f"double(4) = {double(4)}")
    # Wrong type, no error: "ab" * 2 is valid Python, so it just runs.
    print(f"double('ab') = {double('ab')!r}   (a checker would flag this call)")
    print(f"double.__annotations__ = {double.__annotations__}")


def main() -> None:
    not_enforced_demo()


if __name__ == "__main__":
    main()
