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

from collections.abc import Generator
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


def numbered(lines: list[str]) -> Iterator[str]:
    """Yield numbered lines, then *return* how many there were."""
    count = 0
    for line in lines:
        count += 1
        yield f"{count:>2}. {line}"
    return count


def chapters(book: dict[str, list[str]]) -> Iterator[str]:
    total = 0
    for name, lines in book.items():
        yield f"[{name}]"
        # yield from passes the lines through *and* hands back the return value.
        count = yield from numbered(lines)
        total += count
    yield f"total lines: {total}"


def return_value_demo() -> None:
    # A plain for loop ignores the return value. By hand, it arrives as
    # the .value of the StopIteration that ends the generator.
    gen = numbered(["one", "two"])
    print(next(gen))
    print(next(gen))
    try:
        next(gen)
    except StopIteration as stop:
        print(f"StopIteration.value = {stop.value}")

    book = {"intro": ["hello", "welcome"], "body": ["a", "b", "c"]}
    for line in chapters(book):
        print(line)


def spam_filter(limit: int) -> Generator[bool, str, None]:
    """Receive messages; answer True to let one through, False to block it.

    It remembers how often it has seen each message between calls.
    """
    seen: dict[str, int] = {}
    allowed = True
    while True:
        message = yield allowed  # pause: hand out `allowed`, wait for a message
        seen[message] = seen.get(message, 0) + 1
        allowed = seen[message] <= limit


def send_demo() -> None:
    gate = spam_filter(limit=2)
    # Prime it: run to the first yield. A fresh generator is not paused at a
    # yield yet, so there is nowhere for a sent value to go.
    next(gate)

    for message in ["hi", "buy now", "buy now", "hello", "buy now", "buy now"]:
        verdict = gate.send(message)
        print(f"{message!r:<10} -> {'pass' if verdict else 'BLOCKED'}")

    try:
        spam_filter(limit=1).send("too early")
    except TypeError as exc:
        print(f"send() before priming -> TypeError: {exc}")


def main() -> None:
    yield_from_demo()
    print()
    return_value_demo()
    print()
    send_demo()


if __name__ == "__main__":
    main()
