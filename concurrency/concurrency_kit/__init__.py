"""concurrency_kit: RWLock, Future, pool_map, TokenBucket, CircuitBreaker, retry.

    >>> from concurrency.concurrency_kit import ManualClock, TokenBucket, pool_map
    >>> [r.value for r in pool_map(lambda n: n * n, range(5), workers=3)]
    [0, 1, 4, 9, 16]
    >>> clock = ManualClock(); bucket = TokenBucket(rate=1, capacity=2, clock=clock)
    >>> [bucket.allow() for _ in range(3)]
    [True, True, False]
    >>> clock.advance(1); bucket.allow()
    True
"""

from .resilience import (
    CircuitBreaker,
    CircuitOpenError,
    ManualClock,
    State,
    TokenBucket,
    backoff_delays,
    retry_with_backoff,
)
from .threads import Future, Result, RWLock, pool_map

__all__ = [
    "RWLock",
    "Future",
    "Result",
    "pool_map",
    "ManualClock",
    "TokenBucket",
    "CircuitBreaker",
    "CircuitOpenError",
    "State",
    "backoff_delays",
    "retry_with_backoff",
]
