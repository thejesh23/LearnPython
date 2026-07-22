"""Raft leader election: picking one leader per term, by majority vote.

Every node is a follower, a candidate or a leader, and time is divided into
terms numbered by a monotonically increasing integer. A follower that hears
nothing from a leader before its election timeout expires bumps the term,
becomes a candidate, votes for itself and asks everyone else for a vote. Each
node grants at most one vote per term, so at most one candidate can collect a
majority, which is what makes "one leader per term" safe.

Nothing forbids two candidates starting at once and splitting the vote, so a
round can end with no leader. Raft's fix is randomised election timeouts: on
retry the nodes wake at different times, one gets a head start, and the split
becomes very unlikely. This simulation runs the state machine in one process
with a seeded RNG, so the split-vote round below is reproducible.
"""

import random
from enum import Enum


class Role(str, Enum):
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"


class Node:
    def __init__(self, node_id: int, rng: random.Random) -> None:
        self.id = node_id
        self.rng = rng
        self.role = Role.FOLLOWER
        self.term = 0
        self.voted_for: int | None = None
        self.timeout = self.reset_timeout()

    def reset_timeout(self) -> int:
        """Randomised so that nodes rarely time out on the same tick."""
        self.timeout = self.rng.randint(15, 30)
        return self.timeout

    def become_follower(self, term: int) -> None:
        self.role = Role.FOLLOWER
        if term > self.term:
            self.term, self.voted_for = term, None
        self.reset_timeout()

    def request_vote(self, term: int, candidate: int) -> bool:
        if term < self.term:
            return False  # stale candidate; it will learn the newer term
        if term > self.term:
            self.become_follower(term)
        granted = self.voted_for in (None, candidate)
        if granted:
            self.voted_for = candidate
            self.reset_timeout()
        return granted


class Cluster:
    def __init__(self, size: int, seed: int, forced_ties: int = 0) -> None:
        self.rng = random.Random(seed)
        self.nodes = [Node(i, self.rng) for i in range(size)]
        self.majority = size // 2 + 1
        self.forced_ties = forced_ties  # make the first N rounds split the vote
        self.tick_count = 0

    def leader(self) -> Node | None:
        return next((n for n in self.nodes if n.role is Role.LEADER), None)

    def tick(self) -> None:
        self.tick_count += 1
        leader = self.leader()
        if leader is not None:
            for node in self.nodes:  # heartbeats keep followers quiet
                if node is not leader:
                    node.become_follower(leader.term)
            return

        due = []
        for node in self.nodes:
            node.timeout -= 1
            if node.timeout <= 0:
                due.append(node)
        if not due:
            return
        if self.forced_ties and len(due) == 1:
            # Teaching device: drag a second node in so the vote splits.
            due.append(next(n for n in self.nodes if n is not due[0]))
            self.forced_ties -= 1
        self.run_election(due)

    def run_election(self, candidates: list[Node]) -> None:
        """All candidates campaign in the same term, concurrently."""
        term = max(n.term for n in self.nodes) + 1
        for cand in candidates:
            cand.role = Role.CANDIDATE
            cand.term, cand.voted_for = term, cand.id
            cand.reset_timeout()

        votes = {cand.id: 1 for cand in candidates}  # each votes for itself
        voters = [n for n in self.nodes if n not in candidates]
        for i, voter in enumerate(voters):
            # Message ordering differs per voter, so who asks first varies.
            spin = i % len(candidates)
            arrivals = candidates[spin:] + candidates[:spin]
            for cand in arrivals:
                if voter.request_vote(term, cand.id):
                    votes[cand.id] += 1
                    break

        tally = " ".join(f"node{cid}={v}" for cid, v in sorted(votes.items()))
        print(f"  tick {self.tick_count:>3}  term {term}: {tally} "
              f"(needs {self.majority} of {len(self.nodes)})")
        for cand in candidates:
            if votes[cand.id] >= self.majority:
                cand.role = Role.LEADER
                print(f"  tick {self.tick_count:>3}  node {cand.id} is LEADER "
                      f"for term {term}")
                return
        print(f"  tick {self.tick_count:>3}  split vote — no leader in term {term}")


def run(cluster: Cluster, ticks: int) -> None:
    for _ in range(ticks):
        cluster.tick()
        if cluster.leader() is not None:
            return


def main() -> None:
    print("clean election in a 5-node cluster")
    cluster = Cluster(5, seed=3)
    run(cluster, 60)
    leader = cluster.leader()
    assert leader is not None
    print(f"  settled: leader={leader.id} term={leader.term}")
    print(f"  roles: {[n.role.value for n in cluster.nodes]}")

    print("\nforced split vote, resolved on retry")
    cluster = Cluster(4, seed=3, forced_ties=1)  # even size makes ties easy
    run(cluster, 120)
    leader = cluster.leader()
    print(f"  settled: leader={leader.id if leader else None} "
          f"after {cluster.tick_count} ticks")
    print("  the split round elected nobody; randomised timeouts desynchronised "
          "the retry")

    print("\nleader crashes, the survivors elect a new one")
    cluster = Cluster(5, seed=9)
    run(cluster, 60)
    old = cluster.leader()
    assert old is not None
    cluster.nodes = [n for n in cluster.nodes if n is not old]
    cluster.majority = len(cluster.nodes) // 2 + 1
    run(cluster, 120)
    new = cluster.leader()
    print(f"  old leader {old.id} (term {old.term}) removed; "
          f"new leader {new.id if new else None} (term {new.term if new else '-'})")
    print("  the new term is higher, so a returning old leader steps down")

    print("\nedge cases")
    solo = Cluster(1, seed=1)
    run(solo, 60)
    print(f"  1-node cluster elects itself: leader={solo.leader().id}")
    node = Node(0, random.Random(0))
    node.term = 5
    print(f"  vote for a stale term 3 while at term 5: "
          f"{node.request_vote(3, candidate=1)}")
    print(f"  two candidates in one term: {node.request_vote(6, 1)} then "
          f"{node.request_vote(6, 2)}")


if __name__ == "__main__":
    main()
