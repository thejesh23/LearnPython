"""sketch_kit: count-min, HyperLogLog, MinHash, reservoir sampling, Monte Carlo.

    >>> from probabilistic.sketch_kit import CountMinSketch, HyperLogLog
    >>> cms = CountMinSketch()
    >>> for word in "to be or not to be".split(): cms.add(word)
    >>> cms.estimate("to"), cms.estimate("hamlet")
    (2, 0)
    >>> hll = HyperLogLog()
    >>> for n in range(1000): hll.add(n % 300)
    >>> round(hll.count())  # 300 distinct values, estimated
    303
"""

from .sampling import estimate_pi, mc_integrate, reservoir_sample, stratified_integrate
from .sketches import CountMinSketch, HyperLogLog, MinHash, hash64, jaccard, shingles

__all__ = [
    "hash64",
    "CountMinSketch",
    "HyperLogLog",
    "MinHash",
    "shingles",
    "jaccard",
    "reservoir_sample",
    "estimate_pi",
    "mc_integrate",
    "stratified_integrate",
]
