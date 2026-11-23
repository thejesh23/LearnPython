"""distributed_kit: hash ring, vector clocks, CRDTs, two-phase commit, Raft election.

    >>> from distributed.distributed_kit import GCounter, VectorClock
    >>> a, b = VectorClock().tick("p"), VectorClock().tick("q")
    >>> a.concurrent_with(b), a.happens_before(a.merge(b).tick("p"))
    (True, True)
    >>> x, y = GCounter({"x": 2}), GCounter({"y": 3})
    >>> x.merge(y).value() == y.merge(x).merge(x).value() == 5
    True
"""

from .consensus import (
    Participant,
    RaftCluster,
    RaftNode,
    Role,
    TxState,
    two_phase_commit,
)
from .data import GCounter, HashRing, ORSet, VectorClock, stable_hash

__all__ = [
    "HashRing",
    "stable_hash",
    "VectorClock",
    "GCounter",
    "ORSet",
    "Participant",
    "TxState",
    "two_phase_commit",
    "RaftCluster",
    "RaftNode",
    "Role",
]
