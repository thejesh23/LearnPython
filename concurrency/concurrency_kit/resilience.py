"""Protecting a dependency: rate limiting, circuit breaking and retry with backoff.

Each piece takes its clock (and sleep) as a parameter, so tests drive them with
a ``ManualClock`` and never actually wait.
"""

import random
import time
from collections.abc import Callable
from enum import Enum


class ManualClock:
    """A clock you advance by hand; call it to read the time."""

    def __init__(self, start: float = 0.0) -> None:
        self.now = start

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        """Move time forward; doubles as a fake ``sleep``."""
        self.now += seconds


class TokenBucket:
    """Allow bursts of up to ``capacity`` and ``rate`` requests per second on average."""

    def __init__(self, rate: float, capacity: float,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self.rate, self.capacity, self.clock = rate, capacity, clock
        self.tokens = capacity  # start full
        self._updated = clock()

    def allow(self, cost: float = 1.0) -> bool:
        """Spend ``cost`` tokens if available. Refill is computed lazily."""
        now = self.clock()
        self.tokens = min(self.capacity, self.tokens + (now - self._updated) * self.rate)
        self._updated = now
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False


class State(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half-open"


class CircuitOpenError(RuntimeError):
    """Raised instead of calling the dependency while the circuit is open."""


class CircuitBreaker:
    """Trip open after ``threshold`` consecutive failures; probe after ``cooldown``."""

    def __init__(self, threshold: int = 3, cooldown: float = 5.0, trial_successes: int = 2,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self.threshold, self.cooldown, self.clock = threshold, cooldown, clock
        self.trial_successes = trial_successes
        self.state = State.CLOSED
        self.failures = self.successes = 0
        self.opened_at = 0.0

    def _trip(self) -> None:
        self.state, self.opened_at = State.OPEN, self.clock()
        self.failures = self.successes = 0

    def call[T](self, fn: Callable[[], T]) -> T:
        """Call ``fn`` through the breaker, or raise CircuitOpenError without calling."""
        if self.state is State.OPEN and self.clock() - self.opened_at >= self.cooldown:
            self.state, self.successes = State.HALF_OPEN, 0
        if self.state is State.OPEN:
            raise CircuitOpenError("circuit open; request shed")
        try:
            result = fn()
        except Exception:
            self.failures += 1
            if self.state is State.HALF_OPEN or self.failures >= self.threshold:
                self._trip()  # one failed probe is enough to reopen
            raise
        if self.state is State.HALF_OPEN:
            self.successes += 1
            if self.successes >= self.trial_successes:
                self.state, self.failures, self.successes = State.CLOSED, 0, 0
        else:
            self.failures = 0  # only consecutive failures count
        return result


def backoff_delays(attempts: int, base: float, cap: float, jitter: float,
                   rng: random.Random) -> list[float]:
    """Capped exponential delays, each randomised by +/- ``jitter`` of itself."""
    out = []
    for n in range(attempts):
        raw = min(cap, base * 2 ** n)
        out.append(raw * (1 - jitter) + rng.uniform(0, 2 * raw * jitter))
    return out


def retry_with_backoff[T](fn: Callable[[], T], attempts: int = 5, base: float = 0.05,
                          cap: float = 1.0, jitter: float = 0.5,
                          retry_on: tuple[type[Exception], ...] = (TimeoutError, ConnectionError),
                          rng: random.Random | None = None,
                          sleep: Callable[[float], None] = time.sleep) -> T:
    """Call ``fn`` until it succeeds; other exception types propagate at once."""
    delays = backoff_delays(attempts - 1, base, cap, jitter, rng or random.Random())
    for delay in delays:
        try:
            return fn()
        except retry_on:
            sleep(delay)
    return fn()  # final attempt: let its exception reach the caller
