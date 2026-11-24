"""Timeouts, and running blocking code without freezing the event loop.

    asyncio.timeout(s)     a deadline for a whole `async with` block (3.11+)
    asyncio.wait_for(c, s) a deadline for one awaitable (see async_await.py)
    asyncio.to_thread(f)   run a blocking function in a worker thread and
                           await its result

The event loop runs one coroutine at a time and only switches at an `await`.
A blocking call such as `time.sleep`, `urlopen` or a slow file read
never awaits, so while it runs *nothing else* in the program makes progress:
no timers, no other requests, not even a timeout. `to_thread` moves the
blocking call onto a thread so the loop stays free.

Threads help with blocking I/O. For CPU-heavy work in pure Python, threads do
not run in parallel (because of the GIL); use a process pool instead.
"""

import asyncio
import threading
import time


async def step(name: str, seconds: float, done: list[str]) -> None:
    await asyncio.sleep(seconds)
    done.append(name)


async def timeout_block_main() -> None:
    done: list[str] = []
    try:
        # One budget for all three steps together, which wait_for (one
        # awaitable at a time) cannot express as neatly.
        async with asyncio.timeout(0.1):
            await step("connect", 0.02, done)
            await step("login", 0.02, done)
            await step("download", 0.5, done)  # too slow: gets cancelled
    except TimeoutError:
        print(f"deadline hit; finished steps: {done}")

    # The same block with enough time completes normally.
    done.clear()
    async with asyncio.timeout(0.5):
        await step("ping", 0.01, done)
    print(f"within the deadline: {done}")


def timeout_block_demo() -> None:
    asyncio.run(timeout_block_main())


async def heartbeat(ticks: list[int]) -> None:
    """Stands in for everything else the program should keep doing."""
    while True:
        ticks.append(len(ticks))
        await asyncio.sleep(0.01)


async def blocking_main() -> None:
    ticks: list[int] = []
    beat = asyncio.create_task(heartbeat(ticks))
    await asyncio.sleep(0)  # let the heartbeat start

    before = len(ticks)
    time.sleep(0.1)  # WRONG inside async code: no await, the loop is stuck
    print(f"heartbeat ticked during time.sleep:    {len(ticks) > before}")

    before = len(ticks)
    await asyncio.sleep(0.1)  # the loop runs other tasks while we wait
    print(f"heartbeat ticked during asyncio.sleep: {len(ticks) > before}")
    beat.cancel()


def blocking_demo() -> None:
    asyncio.run(blocking_main())


def legacy_download(name: str) -> str:
    """A blocking function we cannot rewrite, e.g. from an older library."""
    time.sleep(0.1)
    return f"{name}.zip"


async def to_thread_main() -> None:
    ticks: list[int] = []
    beat = asyncio.create_task(heartbeat(ticks))
    await asyncio.sleep(0)

    before = len(ticks)
    result = await asyncio.to_thread(legacy_download, "report")
    print(f"got {result!r}; heartbeat kept ticking: {len(ticks) > before}")

    # Several blocking calls now overlap, each on its own thread.
    start = time.perf_counter()
    files = await asyncio.gather(
        *(asyncio.to_thread(legacy_download, n) for n in ("a", "b", "c"))
    )
    elapsed = time.perf_counter() - start
    print(f"{files} in parallel, faster than 3 x 0.1s: {elapsed < 0.25}")
    beat.cancel()


def to_thread_demo() -> None:
    asyncio.run(to_thread_main())


def slow_job(finished: threading.Event) -> None:
    time.sleep(0.15)
    finished.set()


async def timeout_thread_main() -> None:
    finished = threading.Event()
    try:
        async with asyncio.timeout(0.03):
            await asyncio.to_thread(slow_job, finished)
    except TimeoutError:
        print(f"timed out; job finished yet? {finished.is_set()}")

    # Python cannot kill a thread. The job carries on in the background, so
    # blocking work that may hang needs its own timeout (e.g. a socket timeout).
    await asyncio.sleep(0.2)
    print(f"a moment later, job finished?  {finished.is_set()}")


def timeout_thread_demo() -> None:
    asyncio.run(timeout_thread_main())


def main() -> None:
    timeout_block_demo()
    print()
    blocking_demo()
    print()
    to_thread_demo()
    print()
    timeout_thread_demo()


if __name__ == "__main__":
    main()
