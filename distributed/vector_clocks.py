"""Vector clocks: ordering events without a shared clock.

Wall clocks drift and a single counter cannot tell "A caused B" from "A and B
happened independently". A vector clock gives every process a slot in a vector
of counters. A process bumps its own slot on each local event, ships the whole
vector with every message, and on receipt takes the element-wise maximum before
bumping its own slot again.

Comparing two vectors then decides causality exactly: A happens-before B if
every element of A is <= B and at least one is strictly smaller. If neither
dominates the other, the events are concurrent — nobody could have influenced
the other, which is precisely the case where two writes conflict and some merge
policy (last-writer-wins, sibling values, a CRDT) has to step in.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class VectorClock:
    counters: dict[str, int] = field(default_factory=dict)

    def tick(self, pid: str) -> "VectorClock":
        merged = dict(self.counters)
        merged[pid] = merged.get(pid, 0) + 1
        return VectorClock(merged)

    def merge(self, other: "VectorClock") -> "VectorClock":
        keys = self.counters.keys() | other.counters.keys()
        return VectorClock({k: max(self.get(k), other.get(k)) for k in keys})

    def get(self, pid: str) -> int:
        return self.counters.get(pid, 0)  # a missing slot means zero events

    def happens_before(self, other: "VectorClock") -> bool:
        keys = self.counters.keys() | other.counters.keys()
        return (all(self.get(k) <= other.get(k) for k in keys)
                and any(self.get(k) < other.get(k) for k in keys))

    def concurrent_with(self, other: "VectorClock") -> bool:
        return not (self.happens_before(other) or other.happens_before(self)
                    or self == other)

    def __str__(self) -> str:
        inner = ", ".join(f"{k}:{v}" for k, v in sorted(self.counters.items()))
        return "{" + inner + "}"


class Process:
    def __init__(self, pid: str) -> None:
        self.pid = pid
        self.clock = VectorClock()

    def local_event(self, label: str) -> VectorClock:
        self.clock = self.clock.tick(self.pid)
        print(f"  {self.pid} {label:<22} {self.clock}")
        return self.clock

    def send(self, label: str) -> VectorClock:
        return self.local_event(f"send {label}")

    def receive(self, label: str, stamp: VectorClock) -> VectorClock:
        self.clock = self.clock.merge(stamp).tick(self.pid)
        print(f"  {self.pid} recv {label:<17} {self.clock}")
        return self.clock


def relation(a: VectorClock, b: VectorClock) -> str:
    if a == b:
        return "identical"
    if a.happens_before(b):
        return "a -> b (a happens-before b)"
    if b.happens_before(a):
        return "b -> a (b happens-before a)"
    return "concurrent (conflict)"


def main() -> None:
    print("causal chain: A writes, tells B, B tells C")
    a, b, c = Process("A"), Process("B"), Process("C")
    m1 = a.send("m1")
    b.receive("m1", m1)
    m2 = b.send("m2")
    e_c = c.receive("m2", m2)
    print(f"  A's send vs C's receive: {relation(m1, e_c)}")

    print("\nconcurrent updates: two replicas edit the same key unaware")
    x, y = Process("X"), Process("Y")
    shared = VectorClock({"X": 1, "Y": 1})  # both start from the same version
    x.clock = y.clock = shared
    vx = x.local_event("set colour=red")
    vy = y.local_event("set colour=blue")
    print(f"  {vx} vs {vy}: {relation(vx, vy)}")
    print(f"  concurrent_with: {vx.concurrent_with(vy)}")

    print("\nresolving it: X hears Y's version and merges")
    merged = x.receive("colour=blue", vy)
    print(f"  merged vs each parent: {relation(vy, merged)} / {relation(vx, merged)}")

    print("\nedge cases")
    empty = VectorClock()
    print(f"  empty vs empty:            {relation(empty, empty)}")
    print(f"  empty vs {{A:1}}:            {relation(empty, VectorClock({'A': 1}))}")
    lhs, rhs = VectorClock({"A": 2, "B": 1}), VectorClock({"A": 1, "B": 2})
    print(f"  {lhs} vs {rhs}:  {relation(lhs, rhs)}")


if __name__ == "__main__":
    main()
