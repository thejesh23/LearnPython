"""Examples and self-check: python3 -m advanced.toolbox_kit"""

import itertools
import random
import sys
from collections.abc import Callable
from dataclasses import dataclass, field

from . import ConfigError, Field, Pipeline, RetryError, describe, load_config, retry, timed


class Order:
    """Attributes validated by descriptors on every assignment, not just in __init__."""

    quantity = Field(int, check=lambda n: n > 0)
    label = Field(str)

    def __init__(self, quantity: int, label: str) -> None:
        self.quantity, self.label = quantity, label


@dataclass
class ServerConfig:
    host: str = "localhost"
    port: int = 8000
    debug: bool = False
    workers: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not 0 < self.port < 65536:
            raise ValueError(f"port {self.port} out of range")


def flaky(failures: int) -> Callable[[], str]:
    """A timed function that raises ConnectionError ``failures`` times, then succeeds."""
    @timed
    def fetch() -> str:
        """Pretend network call."""
        if fetch.calls < failures:
            raise ConnectionError("dropped")
        return "200 OK"
    return fetch


def examples() -> None:
    @timed
    def total(n: int) -> int:
        """Sum of squares below n."""
        return sum(i * i for i in range(n))
    total(10_000)
    total(10_000)
    print(f"1. timed: {total.__name__!r} ran {total.calls}x, kept its docstring:",
          repr(total.__doc__))

    waits: list[float] = []
    fetch = retry(times=4, on=(ConnectionError,), delay=0.1, sleep=waits.append)(flaky(2))
    print("2. retry:", fetch(), "after waits", waits)
    try:
        retry(times=2, sleep=waits.append)(flaky(5))()
    except RetryError as exc:
        print(f"3. gave up: {exc} | cause: {exc.__cause__!r}")

    print("4. describe:", describe((3, 2.5, "x", False, [None])))

    sevens = Pipeline(itertools.count(1)).filter(lambda n: n % 7 == 0).map(str).batch(3)
    print("5. lazy pipeline over an infinite count:", sevens.take(2))

    order = Order(3, "widgets")
    for bad in ("many", 0):
        try:
            order.quantity = bad
        except (TypeError, ValueError) as exc:
            print(f"6. Field rejected {bad!r}: {type(exc).__name__}: {exc}")

    env = {"SRV_PORT": "9000", "SRV_DEBUG": "yes", "SRV_WORKERS": "1, 2, 4", "PATH": "/usr/bin"}
    print("7. load_config:", load_config(ServerConfig, env, prefix="SRV_"))


def self_check() -> None:
    rng = random.Random(4)
    for _ in range(20):
        failures, times = rng.randint(0, 5), rng.randint(1, 5)
        fetch, waits = flaky(failures), []
        wrapped = retry(times, on=(ConnectionError,), delay=1.0, sleep=waits.append)(fetch)
        try:
            assert wrapped() == "200 OK" and failures < times
            assert waits == [2.0 ** i for i in range(failures)]  # exponential backoff
        except RetryError as exc:
            assert failures >= times and isinstance(exc.__cause__, ConnectionError)
        assert fetch.calls == min(failures + 1, times) and fetch.seconds >= 0
    try:
        retry(on=(KeyError,))(flaky(1))()
    except ConnectionError:
        pass  # not in `on`, so it escapes untouched
    else:
        raise AssertionError("retried an exception it was not told to")

    data = [rng.randint(-50, 50) for _ in range(200)]
    expected = [x * 3 for x in data if x > 0]
    assert Pipeline(data).filter(lambda x: x > 0).map(lambda x: x * 3).take(1000) == expected
    batches = list(Pipeline(data).batch(7))
    assert [x for b in batches for x in b] == data and all(len(b) == 7 for b in batches[:-1])
    pulled: list[int] = []
    lazy = Pipeline(data).map(lambda x: pulled.append(x) or x)
    assert pulled == [] and lazy.take(3) == data[:3] and pulled == data[:3], "not lazy"

    assert describe(True) == "yes" and describe(5) == "the integer 5"
    assert describe({1: 2}) == "a dict"  # falls back to the base implementation

    order = Order(1, "x")
    assert "_quantity" in vars(order) and isinstance(Order.quantity, Field)
    for bad in ("1", -1, 2.0):
        try:
            order.quantity = bad
        except (TypeError, ValueError):
            pass
        else:
            raise AssertionError(f"accepted {bad!r}")
    assert order.quantity == 1

    assert load_config(ServerConfig, {}) == ServerConfig()
    assert load_config(ServerConfig, {"port": 81, "debug": "off"}).debug is False
    for bad in ({"port": "eighty"}, {"debug": "maybe"}, {"colour": "red"}, {"port": "70000"}):
        try:
            load_config(ServerConfig, bad)
        except ConfigError:
            pass
        else:
            raise AssertionError(f"accepted {bad}")


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
