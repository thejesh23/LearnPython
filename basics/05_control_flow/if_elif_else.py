"""`if` / `elif` / `else` — branching, and Python's use of indentation.

Python has no braces. The body of a branch is whatever is indented under the
colon, so indentation is syntax, not style. Four spaces is the convention.

There is no `else if`; the keyword is `elif`. Branches are tested top to
bottom and the first truthy one wins — later ones are never evaluated.

For choosing between two *values* (not two blocks), use the conditional
expression: `a if condition else b`.
"""


def grade(score: int) -> str:
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    else:
        return "F"


def main() -> None:
    for score in (95, 83, 71, 40):
        print(f"{score} -> {grade(score)}")

    # Order matters: a wrong ordering makes later branches unreachable.
    # `if score >= 70` first would classify 95 as "C".

    # Truthiness means you rarely compare to True or to an empty container.
    items: list[int] = []
    if not items:
        print("no items")  # preferred over `if len(items) == 0`

    # Conditional expression — picks a value, not a block.
    n = 7
    parity = "even" if n % 2 == 0 else "odd"
    print(f"{n} is {parity}")

    # Chained comparison keeps range checks flat.
    temperature = 22
    if 18 <= temperature <= 25:
        print("comfortable")

    # `pass` is the do-nothing statement for a body you have not written yet.
    if temperature > 40:
        pass  # TODO: heat warning


if __name__ == "__main__":
    main()
