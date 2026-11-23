"""Agreeing on a decision: two-phase commit and Raft leader election."""

import random
from enum import Enum


class TxState(str, Enum):
    INIT = "init"
    PREPARED = "prepared"  # voted yes: may no longer abort alone
    COMMITTED = "committed"
    ABORTED = "aborted"


class Participant:
    """A resource manager in two-phase commit."""

    def __init__(self, name: str, can_prepare: bool = True) -> None:
        self.name, self.can_prepare = name, can_prepare
        self.state = TxState.INIT

    def prepare(self) -> bool:
        """Phase 1 vote: True means durably prepared and holding locks."""
        self.state = TxState.PREPARED if self.can_prepare else TxState.ABORTED
        return self.can_prepare

    def finish(self, commit: bool) -> None:
        """Phase 2: apply the coordinator's decision."""
        if self.state is TxState.PREPARED:
            self.state = TxState.COMMITTED if commit else TxState.ABORTED

    @property
    def blocked(self) -> bool:
        """Prepared but never told the outcome: stuck with its locks held."""
        return self.state is TxState.PREPARED


def two_phase_commit(participants: list[Participant], crash_after_prepare: bool = False) -> str:
    """Run one round; returns "commit", "abort", or "unknown" if the coordinator dies."""
    votes = [p.prepare() for p in participants]  # every participant is asked
    if crash_after_prepare:
        return "unknown"  # no decision logged or sent: yes-voters now block
    commit = all(votes)
    for p in participants:
        p.finish(commit)
    return "commit" if commit else "abort"


class Role(str, Enum):
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"


class RaftNode:
    """One server: a role, a term, and at most one vote per term."""

    def __init__(self, node_id: int, rng: random.Random) -> None:
        self.id, self.rng = node_id, rng
        self.role, self.term, self.voted_for = Role.FOLLOWER, 0, None
        self.reset_timeout()

    def reset_timeout(self) -> None:
        self.timeout = self.rng.randint(15, 30)  # randomised so ties are rare

    def request_vote(self, term: int, candidate: int) -> bool:
        """Grant a vote unless the term is stale or this term's vote is taken."""
        if term < self.term:
            return False
        if term > self.term:
            self.role, self.term, self.voted_for = Role.FOLLOWER, term, None
        if self.voted_for not in (None, candidate):
            return False
        self.voted_for = candidate
        self.reset_timeout()
        return True


class RaftCluster:
    """Ticks a seeded cluster until one node wins a majority of votes."""

    def __init__(self, size: int, seed: int = 0) -> None:
        self.rng = random.Random(seed)
        self.nodes = [RaftNode(i, self.rng) for i in range(size)]
        self.history: list[tuple[int, dict[int, int], int | None]] = []  # term, votes, winner

    def leader(self) -> RaftNode | None:
        return next((n for n in self.nodes if n.role is Role.LEADER), None)

    def tick(self) -> None:
        """Heartbeat if there is a leader, else count down and maybe hold an election."""
        if (lead := self.leader()) is not None:
            for n in self.nodes:
                if n is not lead:
                    n.role, n.term = Role.FOLLOWER, max(n.term, lead.term)
                    n.reset_timeout()
            return
        for n in self.nodes:
            n.timeout -= 1
        due = [n for n in self.nodes if n.timeout <= 0]
        if due:
            self._elect(due)

    def _elect(self, candidates: list[RaftNode]) -> None:
        term = max(n.term for n in self.nodes) + 1
        for c in candidates:
            c.role, c.term, c.voted_for = Role.CANDIDATE, term, c.id
            c.reset_timeout()
        votes = {c.id: 1 for c in candidates}
        voters = [n for n in self.nodes if n not in candidates]
        for i, voter in enumerate(voters):
            spin = i % len(candidates)  # requests reach each voter in a different order
            for c in candidates[spin:] + candidates[:spin]:
                if voter.request_vote(term, c.id):
                    votes[c.id] += 1
                    break
        winner = next((c for c in candidates if votes[c.id] > len(self.nodes) // 2), None)
        if winner is not None:
            winner.role = Role.LEADER
        self.history.append((term, votes, winner.id if winner else None))

    def run(self, max_ticks: int = 200) -> RaftNode | None:
        """Tick until a leader exists (or give up after ``max_ticks``)."""
        for _ in range(max_ticks):
            self.tick()
            if (lead := self.leader()) is not None:
                return lead
        return None
