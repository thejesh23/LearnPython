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


def main() -> None:
    timeout_block_demo()


if __name__ == "__main__":
    main()
