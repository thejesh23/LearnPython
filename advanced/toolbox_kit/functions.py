"""Function tools: timing and retry decorators, a singledispatch formatter, a lazy pipeline."""

import functools
import itertools
import time
from collections.abc import Callable, Iterable, Iterator
from typing import Any


def timed[**P, R](fn: Callable[P, R]) -> Callable[P, R]:
    """Record call count and elapsed time on ``wrapper.calls`` / ``wrapper.seconds``."""

    @functools.wraps(fn)  # keep __name__, __doc__ and __wrapped__
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()  # monotonic and high resolution, unlike time.time
        try:
            return fn(*args, **kwargs)
        finally:
            wrapper.calls += 1
            wrapper.seconds += time.perf_counter() - start

    wrapper.calls, wrapper.seconds = 0, 0.0
    return wrapper


class RetryError(Exception):
    """Every attempt failed; ``__cause__`` holds the last error."""


def retry(times: int = 3, on: tuple[type[Exception], ...] = (Exception,), delay: float = 0.0,
          sleep: Callable[[float], None] = time.sleep) -> Callable[[Callable], Callable]:
    """Decorator factory: re-run on the listed exceptions, doubling ``delay`` each time."""
    if times < 1:
        raise ValueError("times must be at least 1")

    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(times):
                try:
                    return fn(*args, **kwargs)
                except on as exc:
                    last = exc
                    if attempt + 1 < times:
                        sleep(delay * 2 ** attempt)
            raise RetryError(f"{fn.__name__} failed {times} times") from last
        return wrapper
    return decorator


@functools.singledispatch
def describe(value: object) -> str:
    """Human-readable description chosen by the argument's type."""
    return f"a {type(value).__name__}"


@describe.register(type(None))
def _(value: None) -> str:
    return "nothing"


@describe.register
def _(value: bool) -> str:  # registered separately: bool is a subclass of int
    return "yes" if value else "no"


@describe.register
def _(value: int) -> str:
    return f"the integer {value}"


@describe.register
def _(value: float) -> str:
    return f"the number {value:g}"


@describe.register
def _(value: str) -> str:
    return f"the string {value!r}"


@describe.register(list)
@describe.register(tuple)
def _(value: list | tuple) -> str:
    inner = ", ".join(describe(v) for v in value)  # dispatches again per item
    return f"a {type(value).__name__} of {len(value)}: [{inner}]"


class Pipeline[T]:
    """A lazy chain of generator stages; nothing runs until you consume it."""

    def __init__(self, source: Iterable[T]) -> None:
        self._items: Iterator[Any] = iter(source)

    def map(self, fn: Callable[[Any], Any]) -> "Pipeline":
        return Pipeline(map(fn, self._items))

    def filter(self, pred: Callable[[Any], Any]) -> "Pipeline":
        return Pipeline(filter(pred, self._items))

    def batch(self, size: int) -> "Pipeline":
        """Group items into tuples of ``size`` (the last may be shorter)."""
        return Pipeline(itertools.batched(self._items, size))

    def take(self, n: int) -> list:
        """Pull just ``n`` items through every stage."""
        return list(itertools.islice(self._items, n))

    def __iter__(self) -> Iterator[Any]:
        return self._items
