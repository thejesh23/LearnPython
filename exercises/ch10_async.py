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


def main() -> None:
    check_add_later()


if __name__ == "__main__":
    main()
