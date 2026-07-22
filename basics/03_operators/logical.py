"""`and`, `or`, `not` — words, not symbols, and they return operands.

Python spells the logical operators in English (`&&` and `||` are the *bitwise*
operators `&` and `|`, which do something different).

Two properties matter:
  1. They short-circuit: the right side is not evaluated if the left decides
     the answer. That is what makes `if xs and xs[0]` safe on an empty list.
  2. They return one of the operands, not a bool. `a or b` yields a if a is
     truthy, otherwise b — which is where the "default value" idiom comes from.
"""


def loud(label: str, value: bool) -> bool:
    print(f"  evaluated {label}")
    return value


def main() -> None:
    print("False and loud(...):")
    print(f"  result = {False and loud('right side', True)}")  # not evaluated

    print("True or loud(...):")
    print(f"  result = {True or loud('right side', True)}")  # not evaluated

    print("True and loud(...):")
    print(f"  result = {True and loud('right side', False)}")  # evaluated

    # Short-circuiting guards an unsafe operation.
    xs: list[int] = []
    print(f"xs and xs[0] -> {xs and xs[0]!r}  (no IndexError)")

    # and/or return operands, so `or` supplies a fallback.
    name = ""
    print(f"name or 'anonymous' = {name or 'anonymous'!r}")
    # Careful: this treats every falsy value as missing. When 0 or "" are
    # legitimate values, test for None explicitly instead.
    count = 0
    print(f"count or 10 = {count or 10}  <- probably not what you wanted")
    print(f"10 if count is None else count = {10 if count is None else count}")

    print(f"not '' -> {not ''}   not [1] -> {not [1]}")

    # Bitwise & and | are not logical operators: no short-circuit, and they
    # bind tighter than comparisons.
    print(f"True & False = {True & False}   5 | 2 = {5 | 2}")


if __name__ == "__main__":
    main()
