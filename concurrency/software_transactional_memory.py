"""A tiny software transactional memory: optimistic reads, commit-or-retry.

Instead of locking around a critical section, each transaction runs as if it
were alone. Every shared variable carries a version stamp. Reads record which
version they saw; writes are buffered privately and applied only at commit.
Commit takes a short global lock, checks that every variable read still has the
version it had when read, and if so publishes the buffered writes and bumps
their versions. If any read is stale, someone else committed underneath us, so
nothing is published and the whole transaction re-runs from scratch.

That optimistic scheme means no update is ever lost: two transfers touching the
same account cannot both commit against the same starting balance — one wins,
the other observes the conflict and retries against the fresh value. The commit
lock is held only for the validate-and-publish step, never during user code.
"""

import random
import threading
from typing import Any, Callable, TypeVar

T = TypeVar("T")
_commit_lock = threading.Lock()


class TVar:
    """A transactional variable: a value plus a version that bumps on write."""

    def __init__(self, value: Any) -> None:
        self.value = value
        self.version = 0


class RetryConflict(Exception):
    pass


class Transaction:
    def __init__(self) -> None:
        self._reads: dict[TVar, int] = {}
        self._writes: dict[TVar, Any] = {}

    def read(self, var: TVar) -> Any:
        if var in self._writes:
            return self._writes[var]
        # Record the version so commit can detect a change underneath us.
        self._reads.setdefault(var, var.version)
        return var.value

    def write(self, var: TVar, value: Any) -> None:
        self._writes[var] = value

    def _commit(self) -> bool:
        with _commit_lock:
            for var, seen in self._reads.items():
                if var.version != seen:
                    return False  # stale read: abort, do not publish
            for var, value in self._writes.items():
                var.value = value
                var.version += 1
            return True


def atomically(body: Callable[[Transaction], T]) -> T:
    """Run body in a transaction, retrying until it commits cleanly."""
    while True:
        txn = Transaction()
        result = body(txn)
        if txn._commit():
            return result
        # else: a conflicting commit landed; loop and re-run from scratch.


def main() -> None:
    random.seed(7)
    alice = TVar(100)
    bob = TVar(100)
    retries = [0]
    retry_lock = threading.Lock()

    def transfer(src: TVar, dst: TVar, amount: int) -> Callable[[Transaction], bool]:
        def body(txn: Transaction) -> bool:
            s = txn.read(src)
            if s < amount:
                return False
            txn.write(src, s - amount)
            txn.write(dst, txn.read(dst) + amount)
            return True
        return body

    def run_counting(body: Callable[[Transaction], bool]) -> int:
        """Like atomically, but returns how many attempts commit took."""
        attempts = 0
        while True:
            attempts += 1
            txn = Transaction()
            body(txn)
            if txn._commit():
                return attempts

    def worker(src: TVar, dst: TVar, n: int) -> None:
        for _ in range(n):
            attempts = run_counting(transfer(src, dst, 1))
            with retry_lock:
                retries[0] += attempts - 1

    t1 = threading.Thread(target=worker, args=(alice, bob, 50))
    t2 = threading.Thread(target=worker, args=(bob, alice, 50))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print(f"alice={alice.value}  bob={bob.value}  total={alice.value + bob.value}")
    print(f"total conserved (no lost updates): {alice.value + bob.value == 200}")
    print(f"contended transfers retried {retries[0]} time(s) under the race")

    # A deterministically forced conflict: T1 reads, we let T2 commit under it,
    # then T1 tries to commit and must be rejected and retried.
    shared = TVar(0)
    read_done = threading.Event()
    intruder_done = threading.Event()
    attempts = [0]

    def slow_txn(txn: Transaction) -> int:
        attempts[0] += 1
        seen = txn.read(shared)
        if attempts[0] == 1:  # only stall on the first, doomed attempt
            read_done.set()
            intruder_done.wait(1.0)  # let the intruder bump the version
        txn.write(shared, seen + 1)
        return seen

    def intruder() -> None:
        read_done.wait(1.0)
        atomically(lambda t: t.write(shared, t.read(shared) + 100))
        intruder_done.set()

    ti = threading.Thread(target=intruder)
    ti.start()
    atomically(slow_txn)
    ti.join()
    print(f"forced conflict: first attempt aborted, took {attempts[0]} attempts")
    print(f"both updates survived: shared={shared.value} (100 + 1)")

    print("\nedge cases")
    empty = atomically(lambda txn: "no reads or writes commits immediately")
    print(f"  empty transaction: {empty!r}")

    poor = TVar(0)
    ok = atomically(transfer(poor, alice, 5))
    print(f"  overdraft refused, still commits (as False): {ok}")
    print(f"  live threads at exit: {threading.active_count()} (only MainThread)")


if __name__ == "__main__":
    main()
