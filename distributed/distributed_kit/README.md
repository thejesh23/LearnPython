# distributed_kit

Five distributed-systems ideas as small in-process models: partitioning, causality, convergence, atomic commit and leader election.

```bash
python3 -m distributed.distributed_kit     # seven examples plus a self-check
```

| API | Module | Highlights |
|---|---|---|
| `HashRing`, `stable_hash` | `data.py` | consistent hashing with virtual nodes; adding a node moves ~1/N of keys |
| `VectorClock` | `data.py` | `happens_before` vs `concurrent_with` |
| `GCounter`, `ORSet` | `data.py` | state-based CRDTs; merge is commutative, associative, idempotent |
| `two_phase_commit`, `Participant` | `consensus.py` | one "no" aborts all; a coordinator crash leaves yes-voters blocked |
| `RaftCluster`, `RaftNode` | `consensus.py` | seeded election timeouts, one vote per term, split votes retried |

Standalone versions live next to this folder, e.g. `../raft_leader_election.py`.
