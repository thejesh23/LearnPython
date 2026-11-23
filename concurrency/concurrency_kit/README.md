# concurrency_kit

Thread coordination and dependency protection behind small, testable classes; every timing-based piece takes an injectable clock.

```bash
python3 -m concurrency.concurrency_kit     # seven examples plus a self-check
```

| API | Module | Highlights |
|---|---|---|
| `RWLock` | `threads.py` | shared readers, exclusive writer, waiting writers go first |
| `Future` | `threads.py` | set-once result, `then()` chaining, errors propagate |
| `pool_map`, `Result` | `threads.py` | worker threads with sentinels, results in input order |
| `TokenBucket`, `ManualClock` | `resilience.py` | lazy refill, bursts up to capacity, no real sleeping in tests |
| `CircuitBreaker`, `CircuitOpenError` | `resilience.py` | closed / open / half-open with a cooldown |
| `retry_with_backoff`, `backoff_delays` | `resilience.py` | capped exponential backoff with jitter, retry only listed errors |

Standalone versions live next to this folder, e.g. `../circuit_breaker.py`.
