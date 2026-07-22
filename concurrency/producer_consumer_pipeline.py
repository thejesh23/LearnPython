"""A multi-stage pipeline: bounded queues give you backpressure for free.

Each stage is a group of threads that reads from one queue and writes to the
next, so all stages run concurrently and the slowest one sets the throughput.
The queues are bounded, which is the important part: when a downstream stage
falls behind, its input queue fills, the upstream `put` blocks, and the
producer is throttled automatically. With unbounded queues the same imbalance
would simply grow memory until the process died.

Shutdown travels the same path as the data. The producer puts one sentinel per
first-stage thread; because queues are FIFO and the sentinels go in last, a
thread only sees one after every real item has been taken. The last thread out
of a stage forwards one sentinel per thread of the next stage, so end-of-stream
ripples down the pipeline and every thread returns on its own — no stop flags
to poll, no timeouts, and nothing killed from outside.
"""

import queue
import threading
import time
from collections.abc import Callable
from typing import Any

DONE = object()  # end-of-stream marker: a unique object, never a real value


class Stage:
    def __init__(self, name: str, source: queue.Queue, sink: queue.Queue | None,
                 fn: Callable[[Any], Any], workers: int,
                 downstream_workers: int = 0) -> None:
        self.name = name
        self.source, self.sink, self.fn = source, sink, fn
        self.downstream_workers = downstream_workers
        self.lock = threading.Lock()
        self.remaining = workers
        self.processed = 0
        self.threads = [threading.Thread(target=self._run, name=f"{name}-{i}")
                        for i in range(workers)]

    def _run(self) -> None:
        while True:
            item = self.source.get()
            if item is DONE:
                with self.lock:
                    self.remaining -= 1
                    last_out = self.remaining == 0
                if last_out and self.sink is not None:
                    for _ in range(self.downstream_workers):
                        self.sink.put(DONE)
                return
            result = self.fn(item)
            if self.sink is not None:
                # Blocks while the sink is full — this is the backpressure.
                self.sink.put(result)
            with self.lock:
                self.processed += 1

    def start(self) -> None:
        for t in self.threads:
            t.start()

    def join(self) -> None:
        for t in self.threads:
            t.join()

    def alive(self) -> list[str]:
        return [t.name for t in self.threads if t.is_alive()]


def main() -> None:
    q1: queue.Queue = queue.Queue(maxsize=3)   # producer -> stage1
    q2: queue.Queue = queue.Queue(maxsize=3)   # stage1   -> stage2
    q3: queue.Queue = queue.Queue(maxsize=3)   # stage2   -> sink
    collected: list[str] = []

    def parse(n: int) -> tuple[int, int]:
        time.sleep(0.002)
        return n, n * n

    def enrich(item: tuple[int, int]) -> str:
        time.sleep(0.010)  # the slow stage; it dictates the whole throughput
        n, square = item
        return f"{n}:{square}"

    def collect(item: str) -> None:
        collected.append(item)  # single sink thread, so no lock needed

    stage1 = Stage("stage1", q1, q2, parse, workers=2, downstream_workers=2)
    stage2 = Stage("stage2", q2, q3, enrich, workers=2, downstream_workers=1)
    sink = Stage("sink", q3, None, collect, workers=1)
    for s in (stage1, stage2, sink):
        s.start()

    blocked, high_water = 0, {"q1": 0, "q2": 0, "q3": 0}
    start = time.perf_counter()
    for n in range(20):
        if q1.full():
            blocked += 1  # this put is about to block: the producer is throttled
        q1.put(n)
        for name, q in (("q1", q1), ("q2", q2), ("q3", q3)):
            high_water[name] = max(high_water[name], q.qsize())

    for _ in stage1.threads:
        q1.put(DONE)  # one per first-stage thread; the rest propagate themselves
    for s in (stage1, stage2, sink):
        s.join()
    elapsed = time.perf_counter() - start

    print(f"collected {len(collected)} items, e.g. {collected[:4]}")
    numbers = sorted(int(s.split(":")[0]) for s in collected)
    print(f"  every input made it through: {numbers == list(range(20))}")
    print(f"  processed per stage: stage1={stage1.processed} "
          f"stage2={stage2.processed} sink={sink.processed}")
    print(f"\nqueue high-water marks (maxsize=3): {high_water}")
    print(f"the producer met a full queue {blocked} times — backpressure held "
          "it to the slow stage's rate")
    print(f"wall time {elapsed:.2f}s (20 x 10ms of stage2 work over 2 threads)")
    alive = stage1.alive() + stage2.alive() + sink.alive()
    print(f"threads still alive after shutdown: {alive}")

    print("\nedge case: an empty stream still shuts down cleanly")
    qa: queue.Queue = queue.Queue(maxsize=2)
    qb: queue.Queue = queue.Queue(maxsize=2)
    solo = Stage("solo", qa, qb, lambda x: x, workers=1, downstream_workers=1)
    solo.start()
    qa.put(DONE)
    solo.join()
    print(f"  worker exited: {not solo.alive()}, "
          f"sentinel forwarded downstream: {qb.get() is DONE}")


if __name__ == "__main__":
    main()
