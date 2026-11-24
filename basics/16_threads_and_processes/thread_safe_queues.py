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


def resize_worker(q: queue.Queue[str], finished: list[str]) -> None:
    # A daemon worker that loops forever. No sentinel needed: main waits on
    # q.join() instead, and the daemon dies quietly when the program exits.
    while True:
        image = q.get()
        time.sleep(0.01)  # pretend to resize the image
        finished.append(image)
        q.task_done()  # without this, q.join() below would wait forever


def join_and_maxsize_demo() -> None:
    q: queue.Queue[str] = queue.Queue()
    finished: list[str] = []
    for i in range(3):
        threading.Thread(target=resize_worker, args=(q, finished), daemon=True).start()

    for n in range(6):
        q.put(f"photo{n}.jpg")
    q.join()  # returns once task_done() has been called for all 6 items
    print(f"photos resized when q.join() returned: {len(finished)} of 6")

    # maxsize limits the queue. When it is full, put() waits, which slows a
    # fast producer down to the consumers' pace instead of piling up memory.
    small: queue.Queue[int] = queue.Queue(maxsize=2)
    small.put(1)
    small.put(2)
    print(f"small queue full: {small.full()}")
    try:
        small.put(3, timeout=0.05)  # wait a little, then give up
    except queue.Full:
        print("put() on a full queue timed out with queue.Full")


def main() -> None:
    basics_demo()
    print()
    producer_consumer_demo()
    print()
    join_and_maxsize_demo()


if __name__ == "__main__":
    main()
