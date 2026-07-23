"""A mini event loop: how async/await works underneath, in ~60 lines.

`await` does not block a thread — it *suspends a coroutine* and hands control
back to a scheduler, which resumes it later. This file builds that scheduler
from scratch to show there is no magic: a coroutine is a generator that yields
instructions, and the loop is a queue that runs ready coroutines and reschedules
sleeping ones by their wake time.

An `await` on one of our awaitables reaches `coro.send(None)`, which runs the
coroutine until its next yield. A `sleep` yields a wake-up request; the loop
parks the coroutine in a time-ordered heap and moves on to others. When a
coroutine returns, StopIteration carries its value, which is how a result
propagates back to whoever awaited it.

This is a cooperative scheduler: one coroutine runs at a time and must yield for
others to progress. Real asyncio adds I/O readiness via the OS selector.
"""

import heapq
from collections.abc import Generator


class Sleep:
    """An awaitable that asks the loop to resume us after `delay` ticks."""

    def __init__(self, delay: float) -> None:
        self.delay = delay

    def __await__(self) -> Generator:
        yield ("sleep", self.delay)


class Task:
    def __init__(self, coro: Generator) -> None:
        self.coro = coro
        self.done = False
        self.result = None
        self.waiters: list[Generator] = []


class Loop:
    def __init__(self) -> None:
        self.ready: list[Generator] = []
        self.sleeping: list[tuple[float, int, Generator]] = []  # (wake, seq, coro)
        self.clock = 0.0
        self._seq = 0

    def call_soon(self, coro: Generator) -> None:
        self.ready.append(coro)

    def _park(self, coro: Generator, delay: float) -> None:
        self._seq += 1
        heapq.heappush(self.sleeping, (self.clock + delay, self._seq, coro))

    def run(self, main: Generator) -> None:
        self.ready.append(main)
        while self.ready or self.sleeping:
            if not self.ready:
                # Nothing runnable now: jump the clock to the next wake-up.
                wake, _, coro = heapq.heappop(self.sleeping)
                self.clock = max(self.clock, wake)
                self.ready.append(coro)
            coro = self.ready.pop(0)
            try:
                command = coro.send(None)  # run until the next yield
            except StopIteration:
                continue  # coroutine finished
            if command and command[0] == "sleep":
                self._park(coro, command[1])


async def worker(name: str, delay: float, log: list[str]) -> None:
    log.append(f"{name} start @ t=?")
    await Sleep(delay)
    log.append(f"{name} resumed after {delay}")


async def main_coro(log: list[str]) -> None:
    # Two workers with different delays interleave without threads.
    loop.call_soon(worker("A", 3, log))
    loop.call_soon(worker("B", 1, log))
    await Sleep(5)
    log.append("main done")


def main() -> None:
    global loop
    loop = Loop()
    log: list[str] = []
    loop.run(main_coro(log))

    print("event log (cooperative interleaving, single thread):")
    for line in log:
        print(f"  {line}")

    # B (delay 1) resumes before A (delay 3), though A was scheduled first.
    order = [line for line in log if "resumed" in line]
    print(f"resume order by wake time: {order}")
    print(f"B resumed before A: {order[0].startswith('B')}")
    print("no threads were used — one coroutine ran at a time, yielding at each await")


if __name__ == "__main__":
    main()
