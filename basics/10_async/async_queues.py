"""`asyncio.Queue` — handing work from producers to consumers.

A queue decouples the code that *finds* work from the code that *does* it.
Producers `await queue.put(item)`; consumers `await queue.get()`, which waits
(without blocking the event loop) until an item is available.

Three patterns cover most uses:

    sentinel        put a special "no more items" value so a consumer knows
                    when to stop
    task_done/join  each consumer calls task_done() per item; join() waits
                    until every item put so far has been processed
    maxsize         a bounded queue makes put() wait when it is full, so a
                    fast producer cannot run far ahead of slow consumers
                    (backpressure)

asyncio.Queue is for coroutines in one event loop. For threads, use
queue.Queue instead.
"""

import asyncio


DONE = None  # the sentinel: a value that can never be a real work item


async def producer(queue: asyncio.Queue[str | None], words: list[str]) -> None:
    for word in words:
        await queue.put(word)
        print(f"  produced {word!r}")
        await asyncio.sleep(0)  # give the consumer a turn
    await queue.put(DONE)


async def consumer(queue: asyncio.Queue[str | None]) -> list[str]:
    seen: list[str] = []
    while True:
        item = await queue.get()  # waits here while the queue is empty
        if item is DONE:
            return seen
        print(f"  consumed {item!r}")
        seen.append(item.upper())


async def sentinel_main() -> None:
    queue: asyncio.Queue[str | None] = asyncio.Queue()
    _, result = await asyncio.gather(
        producer(queue, ["red", "green", "blue"]), consumer(queue)
    )
    print(f"consumer returned {result}")


def sentinel_demo() -> None:
    asyncio.run(sentinel_main())


async def worker(queue: asyncio.Queue[int], results: list[str]) -> None:
    while True:
        n = await queue.get()
        try:
            await asyncio.sleep(0)  # pretend to do some I/O
            results.append(f"{n}^2={n * n}")
        finally:
            queue.task_done()  # always mark the item finished, even on error


async def workers_main() -> None:
    queue: asyncio.Queue[int] = asyncio.Queue()
    for n in range(1, 7):
        queue.put_nowait(n)

    results: list[str] = []
    workers = [asyncio.create_task(worker(queue, results)) for _ in range(3)]
    # join() returns once task_done() has been called for every item.
    await queue.join()
    print(f"all items processed, queue empty: {queue.empty()}")
    print(f"results: {sorted(results, key=lambda r: int(r.split('^')[0]))}")

    # The workers loop forever waiting for more, so cancel them explicitly.
    for w in workers:
        w.cancel()
    await asyncio.gather(*workers, return_exceptions=True)
    print(f"workers cancelled: {all(w.cancelled() for w in workers)}")


def workers_demo() -> None:
    asyncio.run(workers_main())


def main() -> None:
    sentinel_demo()
    print()
    workers_demo()


if __name__ == "__main__":
    main()
