"""Examples and self-check: python3 -m distributed.distributed_kit"""

import random
import sys

from . import (
    GCounter,
    HashRing,
    ORSet,
    Participant,
    RaftCluster,
    TxState,
    VectorClock,
    stable_hash,
    two_phase_commit,
)


def moved_keys(ring: HashRing, keys: list[str], new_node: str) -> float:
    """Fraction of keys whose owner changes when ``new_node`` joins."""
    before = {k: ring.get(k) for k in keys}
    ring.add(new_node)
    return sum(before[k] != ring.get(k) for k in keys) / len(keys)


def examples() -> None:
    keys = [f"user:{i}" for i in range(2000)]
    ring = HashRing(["a", "b", "c"])
    naive = sum(stable_hash(k) % 3 != stable_hash(k) % 4 for k in keys) / len(keys)
    print(f"1. adding a 4th node moves {moved_keys(ring, keys, 'd'):.0%} of keys "
          f"(hash % n would move {naive:.0%})")

    p_send = VectorClock().tick("p")
    q_recv = VectorClock().tick("q").merge(p_send).tick("q")
    r_local = VectorClock().tick("r")
    print("2. vector clocks: send -> recv", p_send.happens_before(q_recv),
          "| recv vs unrelated event concurrent", q_recv.concurrent_with(r_local))

    replicas = [GCounter({name: n}) for name, n in (("a", 5), ("b", 3), ("c", 7))]
    merged = GCounter()
    for r in replicas + replicas[::-1]:  # any order, delivered twice
        merged = merged.merge(r)
    print("3. G-Counter after duplicated, reordered gossip:", merged.value())

    phone: ORSet[str] = ORSet()
    for item in ("milk", "bread", "eggs"):
        phone.add(item)
    laptop = phone.merge(ORSet())
    laptop.remove("bread")
    phone.add("bread")  # concurrent re-add: a tag the laptop never saw
    phone.remove("eggs")
    print("4. OR-Set cart after sync:", sorted(phone.merge(laptop).value()))

    for label, ps, crash in (("all yes", [Participant("db"), Participant("queue")], False),
                             ("one no", [Participant("db"), Participant("queue", False)], False),
                             ("crash", [Participant("db"), Participant("queue")], True)):
        decision = two_phase_commit(ps, crash_after_prepare=crash)
        print(f"5. 2PC {label:<7} -> {decision:<7}",
              [(p.name, p.state.value, "BLOCKED" if p.blocked else "") for p in ps])

    cluster = RaftCluster(4, seed=17)
    leader = cluster.run()
    print(f"6. Raft: split vote then leader {leader.id} in term {leader.term};",
          "rounds (term, votes, winner):", cluster.history)

    cluster = RaftCluster(5, seed=3)
    old = cluster.run()
    cluster.nodes.remove(old)  # the leader crashes
    new = cluster.run()
    print(f"7. Raft: leader {old.id} (term {old.term}) crashes, "
          f"survivors elect {new.id} (term {new.term})")


def self_check() -> None:
    rng = random.Random(8)
    keys = [f"k{rng.random()}" for _ in range(3000)]
    ring = HashRing([f"n{i}" for i in range(5)])
    owners = {k: ring.get(k) for k in keys}
    assert 0.05 < moved_keys(ring, keys, "n5") < 0.30  # ideal is 1/6
    ring.remove("n5")
    assert all(ring.get(k) == owners[k] for k in keys), "remove did not restore owners"
    assert HashRing().get("x") is None

    procs = ["p", "q", "r"]
    clocks = {p: VectorClock() for p in procs}
    history = []
    for _ in range(60):
        p = rng.choice(procs)
        if rng.random() < 0.5 and history:
            clocks[p] = clocks[p].merge(rng.choice(history)).tick(p)  # receive
        else:
            clocks[p] = clocks[p].tick(p)
        history.append(clocks[p])
    for a in history:
        for b in history:
            relations = [a.happens_before(b), b.happens_before(a), a.concurrent_with(b), a == b]
            assert sum(relations) == 1, (a, b)  # exactly one relation holds

    counters = [GCounter() for _ in range(4)]
    for _ in range(100):
        rng.choice(counters).increment(rng.choice("abcd"), rng.randint(0, 3))
    expected = GCounter()
    for c in counters:
        expected = expected.merge(c)
    for _ in range(10):
        order = counters * 2
        rng.shuffle(order)
        got = GCounter()
        for c in order:
            got = got.merge(c)
        assert got == expected
    try:
        GCounter().increment("a", -1)
    except ValueError:
        pass
    else:
        raise AssertionError("G-Counter decreased")
    s: ORSet[int] = ORSet()
    s.add(1)
    s.remove(1)
    s.add(1)
    assert s.value() == {1}, "re-add after remove must survive"

    ps = [Participant("a"), Participant("b", can_prepare=False), Participant("c")]
    assert two_phase_commit(ps) == "abort"
    assert all(p.state is TxState.ABORTED and not p.blocked for p in ps)
    assert two_phase_commit([]) == "commit"

    for seed in range(30):
        cluster = RaftCluster(rng.choice([1, 3, 4, 5, 7]), seed)
        leader = cluster.run()
        assert leader is not None, seed
        terms = [term for term, _, _ in cluster.history]
        assert terms == sorted(set(terms)), "terms must strictly increase"
        winners = [w for _, _, w in cluster.history if w is not None]
        assert winners == [leader.id], "exactly one leader, elected in the last round"


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
