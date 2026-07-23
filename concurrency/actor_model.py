"""Actors: independent threads that own their state and talk only by messages.

Each actor is a thread with a private mailbox (a Queue). It processes one
message at a time to completion before touching the next, so its own state is
never seen by anyone else mid-update. That single-consumer discipline is the
whole trick: because no other thread reads or writes an actor's fields, the
actor needs no locks at all. Concurrency lives in the mailboxes, not in shared
memory.

Messages are one-way. To get an answer you hand over a reply channel and let
the actor send back to it. Shutdown is just another message — a poison pill —
so it queues behind the real work and every earlier message is processed first.
Below: a counter actor answering queries, and two actors playing ping-pong.
"""

import threading
from dataclasses import dataclass
from queue import Queue
from typing import Any


@dataclass
class Message:
    kind: str
    payload: Any = None
    reply_to: "Queue[Any] | None" = None


class Actor:
    def __init__(self, name: str) -> None:
        self.name = name
        self.mailbox: Queue[Message] = Queue()
        self._thread = threading.Thread(target=self._loop, name=name)

    def start(self) -> None:
        self._thread.start()

    def send(self, msg: Message) -> None:
        self.mailbox.put(msg)

    def join(self) -> None:
        self._thread.join()

    def _loop(self) -> None:
        while True:
            msg = self.mailbox.get()
            if msg.kind == "stop":  # poison pill: drains after real work
                return
            self.on_message(msg)

    def on_message(self, msg: Message) -> None:
        raise NotImplementedError


class Counter(Actor):
    """State (the count) is private; only this thread ever touches it."""

    def __init__(self) -> None:
        super().__init__("counter")
        self._count = 0

    def on_message(self, msg: Message) -> None:
        if msg.kind == "add":
            self._count += msg.payload  # no lock: single consumer
        elif msg.kind == "get" and msg.reply_to is not None:
            msg.reply_to.put(self._count)


class Player(Actor):
    def __init__(self, name: str, limit: int) -> None:
        super().__init__(name)
        self.limit = limit
        self.partner: Player | None = None
        self.log: list[str] = []

    def on_message(self, msg: Message) -> None:
        n = msg.payload
        self.log.append(f"{self.name} received {msg.kind} {n}")
        if n >= self.limit or self.partner is None:
            return
        reply = "pong" if msg.kind == "ping" else "ping"
        self.partner.send(Message(reply, n + 1))


def main() -> None:
    counter = Counter()
    counter.start()
    for _ in range(5):
        counter.send(Message("add", 2))
    answer: Queue[int] = Queue()
    counter.send(Message("get", reply_to=answer))
    print(f"counter after 5x add(2): {answer.get()}")

    # get is queued behind the adds, so it always sees the final total.
    counter.send(Message("add", 100))
    counter.send(Message("get", reply_to=answer))
    print(f"messages stay ordered per actor: {answer.get()}")
    counter.send(Message("stop"))
    counter.join()

    ping = Player("ping", limit=6)
    pong = Player("pong", limit=6)
    ping.partner, pong.partner = pong, ping
    ping.start()
    pong.start()
    pong.send(Message("ping", 0))  # kick off the rally

    # Let the rally finish, then stop both. stop queues behind the volleys.
    import time
    time.sleep(0.1)
    ping.send(Message("stop"))
    pong.send(Message("stop"))
    ping.join()
    pong.join()
    print(f"rally length: {len(ping.log) + len(pong.log)} messages")
    print(f"first three at pong: {pong.log[:3]}")

    print("\nedge cases")
    empty = Counter()
    empty.start()
    empty.send(Message("stop"))  # stop with an empty mailbox
    empty.join()
    print(f"  clean stop with no work done: not alive = {not empty._thread.is_alive()}")
    print(f"  live threads at exit: {threading.active_count()} (only MainThread)")


if __name__ == "__main__":
    main()
