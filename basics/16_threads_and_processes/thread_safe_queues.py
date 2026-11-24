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


def main() -> None:
    basics_demo()


if __name__ == "__main__":
    main()
