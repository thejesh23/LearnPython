# 10 · Async

`async`/`await` for programs that spend their time waiting.

Read the files in this order; each one runs on its own:

| # | File | What it teaches |
|---|------|-----------------|
| 1 | [`async_await.py`](async_await.py) | `async` / `await` — concurrency for waiting, not for computing. |
| 2 | [`tasks_and_cancellation.py`](tasks_and_cancellation.py) | Tasks, cancellation, and bounding concurrency. |
| 3 | [`async_generators.py`](async_generators.py) | Async generators and `async for` — streaming values that arrive over time. |
| 4 | [`async_queues.py`](async_queues.py) | `asyncio.Queue` — handing work from producers to consumers. |
| 5 | [`timeouts_and_threads.py`](timeouts_and_threads.py) | Timeouts, and running blocking code without freezing the event loop. |
| 6 | [`async_context_managers.py`](async_context_managers.py) | Async context managers — `async with` and the tools in `contextlib`. |

```bash
python3 basics/10_async/async_await.py
```

## Practice

Open [`exercises/ch10_async.py`](../../exercises/ch10_async.py), fill in each function, and run the file until every line says `[solved]`. Stuck? Compare with [`exercises/solutions/ch10_async.py`](../../exercises/solutions/ch10_async.py).

## Going deeper

- [`advanced/asyncio_patterns.py`](../../advanced/asyncio_patterns.py)
- [`advanced/mini_event_loop.py`](../../advanced/mini_event_loop.py)
- [`advanced/contextvars_and_state.py`](../../advanced/contextvars_and_state.py)

---

← [09_classes](../09_classes/) · [11_errors](../11_errors/) →
