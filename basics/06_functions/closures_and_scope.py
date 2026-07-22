"""Closures and the LEGB scope rule.

Python resolves a name by searching four scopes in order:
    Local -> Enclosing (any surrounding function) -> Global -> Builtins.

A *closure* is an inner function that keeps a reference to a variable from its
enclosing function, alive after that function has returned.

Assignment creates a local name by default. To assign to a name from an outer
scope you must say so: `nonlocal` for an enclosing function's variable,
`global` for a module-level one.
"""

counter = 0  # module-level (global)


def make_counter():
    """Return a function that remembers its own count."""
    count = 0

    def increment() -> int:
        nonlocal count  # without this, `count = ...` would create a local
        count += 1
        return count

    return increment


def make_multiplier(factor: int):
    return lambda n: n * factor  # `factor` is captured by the closure


def bump_global() -> None:
    global counter
    counter += 1


def main() -> None:
    c1 = make_counter()
    c2 = make_counter()
    print(f"c1: {c1()} {c1()} {c1()}")
    print(f"c2: {c2()}   <- independent state")

    triple = make_multiplier(3)
    print(f"triple(7) = {triple(7)}")
    print(f"captured cells: {[cell.cell_contents for cell in triple.__closure__]}")

    bump_global()
    bump_global()
    print(f"module-level counter = {counter}")

    # Assigning to a name anywhere in a function makes it local for the
    # *whole* function — so a read that comes earlier fails.
    def broken() -> int:
        seen = counter  # `counter` is local here, because of the line below
        counter = 0  # noqa: F841
        return seen

    try:
        broken()
    except UnboundLocalError as exc:
        print(f"UnboundLocalError: {exc}")

    shadow = 10

    def shows_shadowing() -> None:
        shadow = 99  # a new local, the outer `shadow` is untouched
        print(f"  inner shadow = {shadow}")

    shows_shadowing()
    print(f"outer shadow = {shadow}")


if __name__ == "__main__":
    main()
