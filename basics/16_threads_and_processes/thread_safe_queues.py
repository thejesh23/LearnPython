"""`queue.Queue` — the safe way to pass work between threads.

Sharing a list or a counter between threads needs locks (see
race_conditions_and_locks.py). A Queue has the locking built in: any number of
threads can `put` items in and `get` them out, and each item is handed to
exactly one taker. Most threaded programs are easiest to get right when the
threads share nothing except queues.

    q.put(item)       add an item (waits if a size-limited queue is full)
    q.get()           take the oldest item (waits until one is available)
    q.task_done()     tell the queue one taken item has been fully handled
    q.join()          wait until every item put in has been marked done

The usual shape is *producer / consumer*: some threads make work, others do it.
"""

import queue
import threading
import time


def basics_demo() -> None:
    q: queue.Queue[str] = queue.Queue()
    for job in ["wash", "dry", "fold"]:
        q.put(job)
    print(f"size {q.qsize()}, first out: {q.get()!r} (first in, first out)")

    # get() would wait forever on an empty queue; get_nowait() raises instead.
    q.get()
    q.get()
    try:
        q.get_nowait()
    except queue.Empty:
        print("get_nowait() on an empty queue raised queue.Empty")

    # Two variants with the same thread-safe interface:
    stack: queue.LifoQueue[str] = queue.LifoQueue()  # last in, first out
    for job in ["wash", "dry", "fold"]:
        stack.put(job)
    print(f"LifoQueue gives back: {stack.get()!r}")

    urgent: queue.PriorityQueue[tuple[int, str]] = queue.PriorityQueue()
    for item in [(3, "tidy desk"), (1, "fix outage"), (2, "reply to email")]:
        urgent.put(item)  # smallest first, so (1, ...) comes out first
    print(f"PriorityQueue gives back: {urgent.get()}")


STOP = None  # a "sentinel": a special item that means "no more work"


def producer(q: queue.Queue[int | None], count: int, consumers: int) -> None:
    for n in range(1, count + 1):
        q.put(n)
        time.sleep(0.005)  # work trickles in over time
    # One sentinel per consumer, so every consumer is told to stop.
    for _ in range(consumers):
        q.put(STOP)


def consumer(q: queue.Queue[int | None], done: list[tuple[str, int]]) -> None:
    name = threading.current_thread().name
    while True:
        item = q.get()  # waits here while the queue is empty
        if item is STOP:
            return
        done.append((name, item * item))


def producer_consumer_demo() -> None:
    q: queue.Queue[int | None] = queue.Queue()
    done: list[tuple[str, int]] = []
    consumers = [threading.Thread(target=consumer, args=(q, done), name=f"c{i}")
                 for i in range(2)]
    for c in consumers:
        c.start()
    producer(q, count=8, consumers=len(consumers))
    for c in consumers:
        c.join()

    # Which consumer got which item varies; the set of results does not.
    print(f"squares: {sorted(value for _, value in done)}")
    print(f"both consumers took part: {len({name for name, _ in done}) == 2}")


def main() -> None:
    basics_demo()
    print()
    producer_consumer_demo()


if __name__ == "__main__":
    main()
