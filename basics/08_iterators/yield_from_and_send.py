"""`yield from`, generator return values, `send()` and `close()`.

basics/08_iterators/generators.py shows the everyday use of a generator: a
function that hands out values one `yield` at a time. Generators can do a bit
more, and these extras show up in real code:

    yield from sub()     hand over to another generator until it finishes
    return value         a generator can finish with a result, and
                         `result = yield from sub()` receives it
    gen.send(value)      push a value *into* a paused generator; the
                         `yield` expression evaluates to that value
    gen.close()          stop a generator early; its `finally` blocks run

`send()` turns a generator into a small object with memory: it waits, receives
input, updates its local variables and replies. advanced/generators_as_coroutines.py
builds pipelines from that idea.
"""

from collections.abc import Iterator


def header(title: str) -> Iterator[str]:
    yield "=" * len(title)
    yield title
    yield "=" * len(title)


def bullet_list(items: list[str]) -> Iterator[str]:
    for item in items:
        yield f"  - {item}"


def report(title: str, items: list[str]) -> Iterator[str]:
    # Each `yield from` passes every value of the sub-generator straight
    # through to our caller, as if it were yielded here.
    yield from header(title)
    yield from bullet_list(items)
    yield f"({len(items)} items)"


def report_long_hand(title: str, items: list[str]) -> Iterator[str]:
    # The same thing without yield from: a loop per sub-generator.
    for line in header(title):
        yield line
    for line in bullet_list(items):
        yield line
    yield f"({len(items)} items)"


def yield_from_demo() -> None:
    for line in report("Shopping", ["eggs", "rice", "tea"]):
        print(line)
    same = list(report("x", ["a"])) == list(report_long_hand("x", ["a"]))
    print(f"identical to the long-hand version: {same}")

    # yield from also accepts any iterable, not just generators.
    def letters() -> Iterator[str]:
        yield from "abc"

    print(f"yield from a string: {list(letters())}")


def main() -> None:
    yield_from_demo()


if __name__ == "__main__":
    main()
