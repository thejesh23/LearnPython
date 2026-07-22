"""Two-phase commit: all-or-nothing across independent resource managers.

A coordinator first asks every participant to PREPARE. A participant that
answers yes has durably written enough to be able to commit later, and has
given up the right to abort on its own — it is now uncertain and must hold its
locks until it is told what happened. If all votes are yes the coordinator
logs the decision and sends COMMIT; a single no turns the round into ABORT.

The protocol is safe but not live. If the coordinator dies after collecting
votes and before the decision reaches anyone, the participants cannot decide
between themselves: a yes-voter does not know whether some peer voted no, so
it can neither commit nor abort, and it blocks with its locks held until the
coordinator returns. That single point of failure is exactly what consensus
protocols such as Paxos and Raft remove, by replicating the decision itself
across a majority so that no single crash can strand it.
"""

from enum import Enum


class Vote(str, Enum):
    YES = "yes"
    NO = "no"


class State(str, Enum):
    INIT = "init"
    PREPARED = "prepared"  # uncertain: cannot decide alone
    COMMITTED = "committed"
    ABORTED = "aborted"


class Participant:
    def __init__(self, name: str, can_prepare: bool = True) -> None:
        self.name = name
        self.can_prepare = can_prepare
        self.state = State.INIT
        self.log: list[str] = []

    def prepare(self) -> Vote:
        if not self.can_prepare:  # e.g. a constraint violation or a lock timeout
            self.state = State.ABORTED
            self.log.append("abort (voted no)")
            return Vote.NO
        self.state = State.PREPARED
        self.log.append("prepared (durable, locks held)")
        return Vote.YES

    def commit(self) -> None:
        if self.state is State.PREPARED:
            self.state = State.COMMITTED
            self.log.append("commit")

    def abort(self) -> None:
        if self.state in (State.INIT, State.PREPARED):
            self.state = State.ABORTED
            self.log.append("abort")

    def is_blocked(self) -> bool:
        """Prepared and still waiting for a decision that never came."""
        return self.state is State.PREPARED


class Coordinator:
    def __init__(self, participants: list[Participant]) -> None:
        self.participants = participants
        self.decision: str | None = None

    def run(self, crash_after_prepare: bool = False) -> str:
        votes = {p.name: p.prepare() for p in self.participants}
        summary = ", ".join(f"{k}={v.value}" for k, v in votes.items())
        print(f"  phase 1 votes: {summary or '(none)'}")

        if crash_after_prepare:
            # The decision is not logged and no message is sent.
            print("  coordinator CRASHES before deciding")
            return "unknown"

        self.decision = ("commit" if all(v is Vote.YES for v in votes.values())
                         else "abort")
        print(f"  phase 2 decision: {self.decision} (logged first, then sent)")
        for p in self.participants:
            if self.decision == "commit":
                p.commit()
            else:
                p.abort()
        return self.decision


def show(participants: list[Participant]) -> None:
    for p in participants:
        blocked = "  <-- BLOCKED, holding locks" if p.is_blocked() else ""
        print(f"    {p.name:<10} {p.state.value:<10}{blocked}".rstrip())


def main() -> None:
    print("happy path: every participant votes yes")
    ps = [Participant("accounts"), Participant("ledger"), Participant("audit")]
    Coordinator(ps).run()
    show(ps)

    print("\none participant votes no: everyone aborts")
    ps = [Participant("accounts"), Participant("ledger", can_prepare=False),
          Participant("audit")]
    Coordinator(ps).run()
    show(ps)

    print("\ncoordinator crashes after prepare: the blocking failure mode")
    ps = [Participant("accounts"), Participant("ledger"), Participant("audit")]
    result = Coordinator(ps).run(crash_after_prepare=True)
    print(f"  outcome: {result}")
    show(ps)
    print(f"  blocked participants: {sum(p.is_blocked() for p in ps)}/{len(ps)}")
    print("  they cannot decide among themselves — a peer may have voted no,")
    print("  so committing risks divergence and aborting risks losing a commit.")
    print("  Replicating the decision over a majority (Raft/Paxos) is the fix;")
    print("  three-phase commit trades extra latency for non-blocking recovery.")

    print("\nedge cases")
    empty = Coordinator([])
    print(f"  no participants: decision={empty.run()} (vacuously all yes)")
    p = Participant("solo")
    p.abort()
    p.commit()  # a decided participant ignores a late duplicate message
    print(f"  commit after abort is ignored: {p.state.value}, log={p.log}")


if __name__ == "__main__":
    main()
