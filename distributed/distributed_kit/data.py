"""Where data lives and how replicas converge: a hash ring, vector clocks, CRDTs."""

import bisect
import hashlib
from collections.abc import Hashable, Iterable
from dataclasses import dataclass, field
from itertools import count

_tags = count()  # stands in for a globally unique (replica, sequence) tag


def stable_hash(value: str) -> int:
    """64-bit hash that is the same in every process (built-in hash() is salted)."""
    return int.from_bytes(hashlib.md5(value.encode()).digest()[:8], "big")


class HashRing:
    """Consistent hashing with virtual nodes: resizing moves only ~K/N keys."""

    def __init__(self, nodes: Iterable[str] = (), replicas: int = 100) -> None:
        self.replicas = replicas
        self._owner: dict[int, str] = {}
        self._points: list[int] = []
        for node in nodes:
            self.add(node)

    def add(self, node: str) -> None:
        for i in range(self.replicas):
            point = stable_hash(f"{node}#{i}")
            self._owner[point] = node
            bisect.insort(self._points, point)

    def remove(self, node: str) -> None:
        for i in range(self.replicas):
            point = stable_hash(f"{node}#{i}")
            del self._owner[point]
            self._points.pop(bisect.bisect_left(self._points, point))

    def get(self, key: str) -> str | None:
        """The first node clockwise of the key's hash, or None on an empty ring."""
        if not self._points:
            return None
        idx = bisect.bisect(self._points, stable_hash(key)) % len(self._points)
        return self._owner[self._points[idx]]


@dataclass(frozen=True)
class VectorClock:
    """One counter per process; comparing two clocks decides causality."""

    counters: dict[str, int] = field(default_factory=dict)

    def get(self, pid: str) -> int:
        return self.counters.get(pid, 0)

    def tick(self, pid: str) -> "VectorClock":
        """A new clock with ``pid``'s slot bumped (a local event or a send)."""
        return VectorClock({**self.counters, pid: self.get(pid) + 1})

    def merge(self, other: "VectorClock") -> "VectorClock":
        """Element-wise maximum; follow with ``tick`` when receiving a message."""
        keys = self.counters.keys() | other.counters.keys()
        return VectorClock({k: max(self.get(k), other.get(k)) for k in keys})

    def happens_before(self, other: "VectorClock") -> bool:
        """Every slot <= other's and at least one strictly smaller."""
        keys = self.counters.keys() | other.counters.keys()
        return (all(self.get(k) <= other.get(k) for k in keys)
                and any(self.get(k) < other.get(k) for k in keys))

    def concurrent_with(self, other: "VectorClock") -> bool:
        """Neither clock dominates: the two events could not see each other."""
        return self != other and not (self.happens_before(other) or other.happens_before(self))


@dataclass
class GCounter:
    """Grow-only counter CRDT: per-replica tallies, merged by element-wise max."""

    counts: dict[str, int] = field(default_factory=dict)

    def increment(self, replica: str, amount: int = 1) -> None:
        if amount < 0:
            raise ValueError("a G-Counter only grows")
        self.counts[replica] = self.counts.get(replica, 0) + amount

    def merge(self, other: "GCounter") -> "GCounter":
        keys = self.counts.keys() | other.counts.keys()
        return GCounter({k: max(self.counts.get(k, 0), other.counts.get(k, 0)) for k in keys})

    def value(self) -> int:
        return sum(self.counts.values())


@dataclass
class ORSet[T: Hashable]:
    """Observed-remove set CRDT: a remove only cancels adds it has seen (add wins)."""

    entries: set[tuple[T, int]] = field(default_factory=set)
    removed: set[int] = field(default_factory=set)

    def add(self, item: T) -> None:
        self.entries.add((item, next(_tags)))

    def remove(self, item: T) -> None:
        self.removed |= {tag for element, tag in self.entries if element == item}

    def merge(self, other: "ORSet[T]") -> "ORSet[T]":
        return ORSet(self.entries | other.entries, self.removed | other.removed)

    def value(self) -> set[T]:
        return {e for e, tag in self.entries if tag not in self.removed}
