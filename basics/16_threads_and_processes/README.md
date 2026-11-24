# 16 · Threads and processes

Doing several things at once, safely, and choosing the right tool.

Read the files in this order; each one runs on its own:

| # | File | What it teaches |
|---|------|-----------------|
| 1 | [`threading_basics.py`](threading_basics.py) | Threads — running several pieces of code at the same time in one program. |
| 2 | [`race_conditions_and_locks.py`](race_conditions_and_locks.py) | Race conditions, and the locks that prevent them. |
| 3 | [`thread_safe_queues.py`](thread_safe_queues.py) | `queue.Queue` — the safe way to pass work between threads. |
| 4 | [`thread_and_process_pools.py`](thread_and_process_pools.py) | `concurrent.futures` — pools of threads or processes that run your functions. |
| 5 | [`choosing_concurrency.py`](choosing_concurrency.py) | Threads, processes or asyncio? It depends on what your program is waiting for. |

```bash
python3 basics/16_threads_and_processes/threading_basics.py
```

## Practice

Open [`exercises/ch16_threads_and_processes.py`](../../exercises/ch16_threads_and_processes.py), fill in each function, and run the file until every line says `[solved]`. Stuck? Compare with [`exercises/solutions/ch16_threads_and_processes.py`](../../exercises/solutions/ch16_threads_and_processes.py).

## Going deeper

- [`advanced/gil_threads_processes.py`](../../advanced/gil_threads_processes.py)
- [`advanced/futures_concurrency.py`](../../advanced/futures_concurrency.py)
- [`advanced/thread_synchronisation.py`](../../advanced/thread_synchronisation.py)
- [`concurrency/`](../../concurrency/)

---

← [15_typing](../15_typing/) · [17_os_and_command_line](../17_os_and_command_line/) →
