"""`bool` and `None` — truth and absence.

`True` and `False` are the only two bools, and — a quirk worth knowing —
`bool` is a subclass of `int`, so `True == 1` and `sum([True, True]) == 2`.

`None` is Python's single "no value" object, the equivalent of `null`. There
is exactly one None in a running program, which is why the idiom is
`x is None` (identity) rather than `x == None` (equality, overridable).

Every object also has a *truthiness*. Empty containers, zero, empty strings
and None are falsy; nearly everything else is truthy.
"""


def main() -> None:
    print(f"True == 1 -> {True == 1}")
    print(f"sum([True, True, False]) = {sum([True, True, False])}")

    falsy = [False, 0, 0.0, "", [], {}, set(), None]
    print("falsy values:", [bool(v) for v in falsy])

    truthy = [True, 1, -1, "0", [0], {"k": None}]
    print("truthy values:", [bool(v) for v in truthy])

    # Identity, not equality, is how you test for None.
    value = None
    print(f"value is None -> {value is None}")

    # A common bug: distinguishing "absent" from "present but falsy".
    for candidate in (None, 0, ""):
        if candidate:
            verdict = "truthy"
        elif candidate is None:
            verdict = "absent"
        else:
            verdict = "present but falsy"
        print(f"{candidate!r:>6} -> {verdict}")

    # and/or return one of their operands, not a bool.
    print(f"'' or 'default' = {'' or 'default'!r}")
    print(f"'abc' and 'xyz' = {'abc' and 'xyz'!r}")


if __name__ == "__main__":
    main()
