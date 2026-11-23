# sketch_kit

Probabilistic data structures and sampling: answers that are approximately right, in a fraction of the memory or time, and reproducible because every hash and RNG is seeded.

```bash
python3 -m probabilistic.sketch_kit     # seven examples plus a self-check
```

| API | Module | Answers |
|---|---|---|
| `CountMinSketch` | `sketches.py` | how often has this item appeared? (never an undercount) |
| `HyperLogLog` | `sketches.py` | how many distinct items? (~1.6% error at the default 4 KB) |
| `MinHash`, `shingles`, `jaccard` | `sketches.py` | how similar are these two sets? |
| `hash64` | `sketches.py` | a seedable 64-bit hash, stable across processes |
| `reservoir_sample` | `sampling.py` | a uniform sample of k items from a stream of unknown length |
| `estimate_pi`, `mc_integrate`, `stratified_integrate` | `sampling.py` | Monte Carlo estimates, plain and stratified |

Standalone versions live next to this folder, e.g. `../hyperloglog.py`.
