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


def main() -> None:
    sentinel_demo()


if __name__ == "__main__":
    main()
