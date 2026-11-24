"""Compressing data and bundling files: `gzip`, `zipfile`, `tarfile`, `shutil`.

Two different jobs that often go together:

    compression   make bytes smaller by describing repeats   gzip
    archiving     pack many files and folders into one       zip, tar

A .zip file does both: each member is compressed on its own. A .tar file only
bundles; .tar.gz then gzips the whole bundle. `shutil.make_archive` builds
either kind from a folder in one call.

Compression works by finding repetition, so the ratio depends entirely on the
data: log files and CSV shrink a lot, random bytes do not shrink at all, and
already-compressed files (JPEG, MP3, .zip) barely change.

Archives from other people deserve care: a member named "../../.bashrc"
would be written outside the target folder. The last parts show the safe way
to extract. Everything is written inside a TemporaryDirectory.
"""

import gzip
import random
import tempfile
from pathlib import Path


def ratio(original: bytes, compressed: bytes) -> str:
    share = len(compressed) / len(original)
    return f"{len(original):>6} -> {len(compressed):>6} bytes ({share:.1%} of the size)"


def gzip_demo() -> None:
    rng = random.Random(42)
    samples = {
        "repetitive log": b"INFO request handled in 12ms\n" * 1000,
        "english text": b" ".join(
            rng.choice([b"the", b"cat", b"sat", b"on", b"a", b"warm", b"mat"])
            for _ in range(5000)),
        "random bytes": rng.randbytes(20_000),
    }
    for label, data in samples.items():
        # mtime=0 leaves the timestamp out, so the output is the same each run.
        packed = gzip.compress(data, mtime=0)
        assert gzip.decompress(packed) == data  # lossless: every byte comes back
        print(f"  {label:<15} {ratio(data, packed)}")

    # Compressing twice gains nothing: the output already looks random.
    once = gzip.compress(samples["english text"], mtime=0)
    print(f"  {'gzip of gzip':<15} {ratio(once, gzip.compress(once, mtime=0))}")

    # gzip.open reads and writes .gz files like ordinary files.
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "app.log.gz"
        with gzip.open(path, "wt", encoding="utf-8") as f:
            for n in range(500):
                f.write(f"line {n}: all systems normal\n")
        with gzip.open(path, "rt", encoding="utf-8") as f:
            lines = f.readlines()
        print(f"app.log.gz on disk: {path.stat().st_size} bytes, "
              f"{len(lines)} lines inside, last: {lines[-1].strip()!r}")


def main() -> None:
    gzip_demo()


if __name__ == "__main__":
    main()
