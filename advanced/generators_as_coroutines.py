"""Generators as coroutines: `send`, `throw`, `close`, and pipelines.

A generator is not only a producer. `send(value)` makes the paused `yield`
expression evaluate to `value`, turning the generator into a *consumer* that
keeps state between calls. This is the mechanism `async`/`await` was built on
before it got its own syntax.

Three details:
  - A generator must be primed (`next(gen)`) before the first `send`.
  - `throw` raises an exception *at the yield point*, so the generator can
    handle it and continue.
  - `close` raises GeneratorExit; cleanup belongs in `finally`.
"""

from collections.abc import Generator


def averager() -> Generator[float, float, None]:
    """A running average that keeps its state between sends."""
    total, count, average = 0.0, 0, 0.0
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count


def primed(fn):
    """Decorator that advances a coroutine to its first yield."""

    def start(*args, **kwargs):
        gen = fn(*args, **kwargs)
        next(gen)
        return gen

    return start


@primed
def printer(prefix: str) -> Generator[None, str, None]:
    try:
        while True:
            message = yield
            print(f"  {prefix}: {message}")
    except GeneratorExit:
        print(f"  {prefix}: closing")
    finally:
        print(f"  {prefix}: cleaned up")


@primed
def uppercase(target) -> Generator[None, str, None]:
    while True:
        message = yield
        target.send(message.upper())


@primed
def only_long(target, minimum: int) -> Generator[None, str, None]:
    while True:
        message = yield
        if len(message) >= minimum:
            target.send(message)


def resilient() -> Generator[int, None, None]:
    n = 0
    while True:
        try:
            yield n
            n += 1
        except ValueError:
            print("  recovered from a thrown ValueError")
            n = 0


def main() -> None:
    print("send: a stateful consumer")
    avg = averager()
    next(avg)  # prime
    for value in (10, 20, 60):
        print(f"  sent {value}, average now {avg.send(value):.2f}")

    print("a pipeline of coroutines (filter -> upper -> print):")
    pipeline = only_long(uppercase(printer("out")), minimum=4)
    for word in ("hi", "hello", "worlds", "no"):
        pipeline.send(word)
    pipeline.close()

    print("throw: inject an exception at the yield point")
    gen = resilient()
    print(f"  {next(gen)}, {next(gen)}, {next(gen)}")
    gen.throw(ValueError)
    print(f"  after throw: {next(gen)}")
    gen.close()

    print("this send/throw/close machinery is what async/await compiles onto")


if __name__ == "__main__":
    main()
