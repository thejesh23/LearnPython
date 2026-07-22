"""`:=` — the walrus operator: assign *and* produce a value in one expression.

Plain `=` is a statement in Python, so you cannot write `if (n = len(xs)) > 3`.
The walrus operator (3.8+) fills that gap: it binds a name and evaluates to the
value, which lets you avoid computing something twice or duplicating a call.

Use it where it removes a repetition. Skip it where it just packs two ideas
onto one line.
"""


def expensive(n: int) -> int:
    print(f"  computing f({n})")
    return n * n


def main() -> None:
    values = [1, 2, 3, 4, 5]

    # Without the walrus: either call twice, or add a line before the `if`.
    if (n := len(values)) > 3:
        print(f"list has {n} items — more than 3")

    # In a comprehension: compute once, filter and keep the same result.
    kept = [y for x in values if (y := expensive(x)) > 4]
    print(f"kept = {kept}")

    # The classic read-until-sentinel loop, without duplicating the read.
    lines = iter(["alpha", "beta", "", "never reached"])
    while (line := next(lines, "")) != "":
        print(f"line: {line}")

    # Reusing a match result instead of searching twice.
    import re

    text = "order-42"
    if (m := re.search(r"\d+", text)) is not None:
        print(f"order number = {m.group()}")

    # Parentheses are usually required: `:=` binds loosely.
    print(f"total = {(total := sum(values))}, doubled = {total * 2}")


if __name__ == "__main__":
    main()
