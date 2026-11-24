"""Practice: async and await (chapter 10).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch10_async.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch10_async.py: try first, peek second. The lessons
for this chapter are in basics/10_async/.
"""

import asyncio
import inspect
from collections.abc import AsyncIterator
from collections.abc import Awaitable
from collections.abc import Callable
from typing import Any


def verdict(error: BaseException) -> str:
    """Turn the exception a test raised into a short status."""
    # A stub raises NotImplementedError. Other errors may wrap it, so follow
    # the chain of causes (and look inside exception groups) before deciding.
    link: BaseException | None = error
    for _ in range(20):
        if link is None:
            break
        if isinstance(link, NotImplementedError):
            return "[todo] not attempted"
        if isinstance(link, BaseExceptionGroup) and link.subgroup(
            NotImplementedError
        ):
            return "[todo] not attempted"
        link = link.__cause__ or link.__context__
    if isinstance(error, AssertionError):
        return f"[not yet] {str(error) or 'a check failed'}"
    return f"[not yet] {type(error).__name__}: {error}"


def report(title: str, test: Callable[[Any], None], impl: Any) -> None:
    """Run one test against one implementation and print a one-line status."""
    try:
        test(impl)
        status = "[solved]"
    except KeyboardInterrupt:
        raise
    except BaseException as error:  # never crash: one line per exercise
        status = verdict(error)
    print(f"{title:<40} {status}")


# --- Exercise 1 -------------------------------------------------------------

async def add_later(a: int, b: int, delay: float) -> int:
    """Wait `delay` seconds without blocking, then return a + b.

    Use `await asyncio.sleep(delay)`, not time.sleep(): while this coroutine
    waits, the event loop must be free to run other tasks.

    >>> asyncio.run(add_later(2, 3, 0.01))
    5
    """
    raise NotImplementedError


def test_add_later(impl: Callable[[int, int, float], Any]) -> None:
    assert inspect.iscoroutinefunction(impl), "define it with async def"
    result = asyncio.run(impl(2, 3, 0.01))
    assert result == 5, f"add_later(2, 3, 0.01) should be 5, got {result}"
    assert asyncio.run(impl(-1, 1, 0)) == 0, "add_later(-1, 1, 0) should be 0"

    async def others_ran_during_wait() -> bool:
        seen: list[str] = []

        async def other() -> None:
            seen.append("other task ran")

        task = asyncio.create_task(other())
        await impl(1, 1, 0.01)
        ran = bool(seen)  # True only if add_later gave the loop a turn
        await task
        return ran

    assert asyncio.run(others_ran_during_wait()), (
        "other tasks should run while add_later waits: use await asyncio.sleep"
    )


def check_add_later() -> None:
    report("1. add_later", test_add_later, add_later)


# --- Exercise 2 -------------------------------------------------------------

async def fetch_all(
    fetch: Callable[[str], Awaitable[str]], names: list[str]
) -> list[str]:
    """Call `await fetch(name)` for every name, all at the same time.

    Return the results in the same order as `names`, even though the fetches
    may finish in a different order. asyncio.gather does both jobs.

    >>> async def shout(name: str) -> str:
    ...     return name.upper()
    >>> asyncio.run(fetch_all(shout, ["ana", "bo"]))
    ['ANA', 'BO']
    """
    raise NotImplementedError


def test_fetch_all(impl: Callable[..., Any]) -> None:
    running = peak = 0

    async def fetch(name: str) -> str:
        nonlocal running, peak
        running += 1
        peak = max(peak, running)
        await asyncio.sleep(0.01 * (len(name) % 3))  # finish out of order
        running -= 1
        return name.upper()

    names = ["ana", "bo", "cy", "dee", "ed"]
    result = asyncio.run(impl(fetch, names))
    expected = [name.upper() for name in names]
    assert result == expected, f"expected {expected}, got {result}"
    assert peak == len(names), (
        f"all {len(names)} fetches should run at once, but at most {peak} did"
    )
    assert asyncio.run(impl(fetch, [])) == [], "no names should give []"


def check_fetch_all() -> None:
    report("2. fetch_all", test_fetch_all, fetch_all)


# --- Exercise 3 -------------------------------------------------------------

async def with_timeout(
    make: Callable[[], Awaitable[str]], seconds: float, default: str
) -> str:
    """Return `await make()`, or `default` if it takes longer than `seconds`.

    make is a function that creates the coroutine (call it: make()). Use
    `async with asyncio.timeout(seconds):` or asyncio.wait_for, and catch
    TimeoutError. Any other error from make() must still reach the caller:
    only a timeout turns into the default.
    """
    raise NotImplementedError


def test_with_timeout(impl: Callable[..., Any]) -> None:
    async def quick() -> str:
        await asyncio.sleep(0)
        return "fast"

    async def slow() -> str:
        await asyncio.sleep(0.5)
        return "slow"

    async def broken() -> str:
        raise KeyError("missing")

    result = asyncio.run(impl(quick, 0.5, "default"))
    assert result == "fast", f"a quick call should return its value, got {result!r}"
    result = asyncio.run(impl(slow, 0.05, "default"))
    assert result == "default", (
        f"a call that times out should give the default, got {result!r}"
    )
    try:
        asyncio.run(impl(broken, 0.5, "default"))
    except KeyError:
        pass
    else:
        raise AssertionError("errors other than a timeout should not be swallowed")


def check_with_timeout() -> None:
    report("3. with_timeout", test_with_timeout, with_timeout)


# --- Exercise 4 -------------------------------------------------------------

async def countdown(start: int, delay: float) -> AsyncIterator[int]:
    """Yield start, start - 1, ..., 1, waiting `delay` seconds before each.

    An `async def` that contains `yield` is an async generator; the caller
    reads it with `async for`. countdown(0, ...) yields nothing.

    >>> async def collect() -> list[int]:
    ...     return [n async for n in countdown(3, 0.01)]
    >>> asyncio.run(collect())
    [3, 2, 1]
    """
    raise NotImplementedError
    yield 0  # never reached: it only makes this stub an async generator


def test_countdown(impl: Callable[[int, float], Any]) -> None:
    assert inspect.isasyncgenfunction(impl), "use yield inside the async def"

    async def collect(start: int) -> list[int]:
        return [n async for n in impl(start, 0.001)]

    result = asyncio.run(collect(3))
    assert result == [3, 2, 1], f"countdown(3) gave {result}, expected [3, 2, 1]"
    assert asyncio.run(collect(1)) == [1], "countdown(1) should yield just 1"
    assert asyncio.run(collect(0)) == [], "countdown(0) should yield nothing"

    async def first_two() -> list[int]:
        taken: list[int] = []
        async for n in impl(1_000_000, 0):  # lazy: only produces what is asked
            taken.append(n)
            if len(taken) == 2:
                break
        return taken

    result = asyncio.run(first_two())
    assert result == [1_000_000, 999_999], f"taking two values gave {result}"


def check_countdown() -> None:
    report("4. countdown", test_countdown, countdown)


# --- Exercise 5 -------------------------------------------------------------

async def bounded_map(
    func: Callable[[int], Awaitable[int]], items: list[int], limit: int
) -> list[int]:
    """Run `await func(item)` for every item, at most `limit` at a time.

    Real code does this to stay polite to a server: start everything, but let
    only a few requests be in flight at once. Wrap each call in
    `async with semaphore:` (an asyncio.Semaphore(limit)) and gather them.
    Results come back in the same order as items.
    """
    raise NotImplementedError


def test_bounded_map(impl: Callable[..., Any]) -> None:
    running = peak = 0

    async def double(n: int) -> int:
        nonlocal running, peak
        running += 1
        peak = max(peak, running)
        await asyncio.sleep(0.005)
        running -= 1
        return n * 2

    for limit in (3, 1, 50):
        running = peak = 0
        items = list(range(10))
        result = asyncio.run(impl(double, items, limit))
        assert result == [n * 2 for n in items], f"limit={limit}: got {result}"
        expected_peak = min(limit, len(items))
        assert peak == expected_peak, (
            f"limit={limit}: expected {expected_peak} running at once, saw {peak}"
        )


def check_bounded_map() -> None:
    report("5. bounded_map", test_bounded_map, bounded_map)


def main() -> None:
    check_add_later()
    check_fetch_all()
    check_with_timeout()
    check_countdown()
    check_bounded_map()


if __name__ == "__main__":
    main()
