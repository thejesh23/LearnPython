"""`*args` and `**kwargs` — variadic parameters, and the unpacking operators.

In a `def`, `*args` collects extra positional arguments into a tuple and
`**kwargs` collects extra keyword arguments into a dict.

At a *call site* the same symbols do the reverse: `f(*xs)` spreads a sequence
into positional arguments, and `f(**d)` spreads a dict into keyword arguments.
Collecting and spreading are mirror images — that is why wrappers can forward
arguments blindly with `f(*args, **kwargs)`.
"""


def total(*args: float) -> float:
    """Sum any number of positional arguments."""
    return sum(args)


def tag(name: str, /, *children: str, **attrs: str) -> str:
    """Build an HTML-ish tag.

    `/` marks everything before it as positional-only, so `name` can never be
    swallowed as a keyword attribute.
    """
    rendered = "".join(f' {k}="{v}"' for k, v in attrs.items())
    return f"<{name}{rendered}>{''.join(children)}</{name}>"


def trace(fn):
    """A wrapper that forwards whatever it is given, unchanged."""

    def wrapper(*args, **kwargs):
        print(f"  calling {fn.__name__} with args={args} kwargs={kwargs}")
        return fn(*args, **kwargs)

    return wrapper


def main() -> None:
    print(f"total() = {total()}")
    print(f"total(1, 2, 3) = {total(1, 2, 3)}")

    print(tag("p", "hello", " world", id="intro", **{"class": "lead"}))

    # Positional-only: `name` cannot be passed by keyword.
    try:
        tag(name="p")  # type: ignore[misc]
    except TypeError as exc:
        print(f"TypeError: {exc}")

    # Spreading at the call site.
    numbers = [1, 2, 3, 4]
    print(f"total(*numbers) = {total(*numbers)}")
    options = {"id": "x", "title": "hi"}
    print(tag("div", "body", **options))

    print("forwarding wrapper:")
    traced_total = trace(total)
    print(f"  result = {traced_total(1, 2, 3)}")


if __name__ == "__main__":
    main()
