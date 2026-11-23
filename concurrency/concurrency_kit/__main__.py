"""Examples and self-check: python3 -m concurrency.concurrency_kit"""

import random
import sys
import threading
import time
from collections.abc import Callable

from . import (
    CircuitBreaker,
    CircuitOpenError,
    Future,
    ManualClock,
    RWLock,
    State,
    TokenBucket,
    backoff_delays,
    pool_map,
    retry_with_backoff,
)


def flaky(fail_times: int, error: Exception) -> Callable[[], str]:
    """A callable that raises ``error`` for its first ``fail_times`` calls."""
    calls = [0]

    def call() -> str:
        calls[0] += 1
        if calls[0] <= fail_times:
            raise error
        return f"ok after {calls[0]} calls"
    return call


def readers_overlap(lock: RWLock, readers: int) -> bool:
    """True if ``readers`` threads can all be inside ``lock.read()`` at once."""
    meet = threading.Barrier(readers, timeout=2)  # only passes if all are inside together
    ok = [True] * readers

    def reader(i: int) -> None:
        with lock.read():
            try:
                meet.wait()
            except threading.BrokenBarrierError:
                ok[i] = False

    threads = [threading.Thread(target=reader, args=(i,)) for i in range(readers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return all(ok)


def examples() -> None:
    def slow_square(n: int) -> int:
        time.sleep(0.005)
        if n == 3:
            raise ValueError("three refuses")
        return n * n
    results = pool_map(slow_square, range(6), workers=3)
    print("1. pool_map in input order:", [r.value if r.ok else repr(r.error) for r in results])

    print("2. four readers share an RWLock at once:", readers_overlap(RWLock(), 4))

    fut = Future()
    doubled = fut.then(lambda x: x * 2)  # attached before the value exists
    producer = threading.Thread(target=lambda: (time.sleep(0.01), fut.set_result(21)))
    producer.start()
    print("3. future:", fut.result(timeout=1), "-> then(x*2):", doubled.result(timeout=1))
    producer.join()

    clock = ManualClock()
    bucket = TokenBucket(rate=2, capacity=3, clock=clock)
    burst = [bucket.allow() for _ in range(5)]
    clock.advance(1.0)
    print("4. token bucket burst:", burst, "| after 1s:", [bucket.allow() for _ in range(3)])

    breaker = CircuitBreaker(threshold=2, cooldown=5, trial_successes=1, clock=clock)
    trail = []
    for fn in (flaky(9, TimeoutError()),) * 3:
        try:
            breaker.call(fn)
        except (TimeoutError, CircuitOpenError) as exc:
            trail.append(f"{type(exc).__name__}->{breaker.state.value}")
    clock.advance(5)
    trail.append(f"{breaker.call(lambda: 'ok')}->{breaker.state.value}")
    print("5. circuit breaker:", trail)

    delays = backoff_delays(5, base=0.1, cap=1.0, jitter=0.0, rng=random.Random(0))
    print("6. backoff without jitter:", delays)
    waited: list[float] = []
    out = retry_with_backoff(flaky(2, ConnectionError()), rng=random.Random(1), sleep=waited.append)
    print("7. retry:", out, "| slept", [round(w, 3) for w in waited])


def self_check() -> None:
    rng = random.Random(3)
    nums = [rng.randint(-50, 50) for _ in range(40)]
    assert [r.value for r in pool_map(abs, nums, workers=5)] == [abs(n) for n in nums]
    assert pool_map(abs, []) == []

    lock, inside, worst = RWLock(), [0], [0]
    guard = threading.Lock()

    def writer() -> None:
        for _ in range(50):
            with lock.write():
                with guard:
                    inside[0] += 1
                    worst[0] = max(worst[0], inside[0])
                with guard:
                    inside[0] -= 1
    threads = [threading.Thread(target=writer) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert worst[0] == 1, "two writers held the lock together"
    assert readers_overlap(lock, 3)

    fut = Future()
    fut.set_exception(KeyError("x"))
    chained = fut.then(lambda v: v + 1)
    for f in (fut, chained):
        try:
            f.result(timeout=0)
        except KeyError:
            pass
        else:
            raise AssertionError("error did not propagate down the chain")
    try:
        fut.set_result(1)
    except RuntimeError:
        pass
    else:
        raise AssertionError("future settled twice")

    clock = ManualClock()
    bucket = TokenBucket(rate=5, capacity=5, clock=clock)
    allowed = 0
    for _ in range(200):  # 20 seconds of 10 requests/second
        clock.advance(0.1)
        allowed += bucket.allow()
    assert 100 <= allowed <= 105, allowed  # long-run rate, plus at most one burst

    breaker = CircuitBreaker(threshold=3, cooldown=1, clock=clock)
    for pattern in (True, False, True, True):  # a success resets the count
        try:
            breaker.call(flaky(1 if pattern else 0, ValueError()))
        except ValueError:
            pass
    assert breaker.state is State.CLOSED
    calls = flaky(5, TimeoutError())
    try:
        retry_with_backoff(calls, attempts=3, sleep=lambda s: None)
    except TimeoutError:
        pass
    else:
        raise AssertionError("retry swallowed the last error")
    try:
        retry_with_backoff(flaky(1, ValueError()), sleep=lambda s: 1 / 0)
    except ValueError:
        pass  # not retryable, so it never slept
    for d, raw in zip(backoff_delays(8, 0.05, 1.0, 0.5, rng), [0.05, 0.1, 0.2, 0.4, 0.8, 1, 1, 1]):
        assert raw * 0.5 <= d <= raw * 1.5
    assert threading.active_count() == 1, "a thread was left running"


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
