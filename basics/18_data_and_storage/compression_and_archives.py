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
import io
import random
import tarfile
import tempfile
import zipfile
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


def make_files(root: Path) -> Path:
    """Create a small folder of files to archive."""
    src = root / "report"
    (src / "data").mkdir(parents=True)
    (src / "README.txt").write_text("Quarterly report\n" * 20, encoding="utf-8")
    rows = "".join(f"{n},{n * n}\n" for n in range(300))
    (src / "data" / "squares.csv").write_text(rows, encoding="utf-8")
    (src / "logo.bin").write_bytes(random.Random(1).randbytes(2000))
    return src


def zipfile_demo() -> None:
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        src = make_files(root)
        archive = root / "report.zip"
        # ZIP_DEFLATED compresses; the default, ZIP_STORED, only bundles.
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(src.rglob("*")):
                if path.is_file():
                    # arcname is the name inside the zip, relative and with '/'.
                    zf.write(path, arcname=path.relative_to(src).as_posix())
            zf.writestr("notes/generated.txt", "made without a file on disk")

        with zipfile.ZipFile(archive) as zf:
            print("members (size -> compressed size):")
            for info in zf.infolist():
                print(f"  {info.filename:<22} {info.file_size:>5} -> "
                      f"{info.compress_size:>5}")
            # Read one member straight into memory, no extraction needed.
            third = zf.read("data/squares.csv").decode().splitlines()[2]
            print(f"third line of squares.csv: {third!r}")
            print(f"testzip() finds no damaged member: {zf.testzip() is None}")

            # extractall: zipfile strips '..' and leading '/' from names.
            out = root / "unzipped"
            zf.extractall(out)
            print(f"extracted {sum(1 for p in out.rglob('*') if p.is_file())} files")


def tarfile_demo() -> None:
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        src = make_files(root)
        archive = root / "report.tar.gz"
        # "w:gz" means: write a tar, gzip the whole thing.
        with tarfile.open(archive, "w:gz") as tf:
            tf.add(src, arcname="report")  # adds the folder recursively
        with tarfile.open(archive, "r:gz") as tf:
            names = sorted(m.name for m in tf.getmembers() if m.isfile())
            print(f"tar.gz is {archive.stat().st_size} bytes, files: {names}")
            # filter="data" refuses links and paths that escape the folder.
            tf.extractall(root / "untarred", filter="data")
        print(f"extracted: {(root / 'untarred/report/README.txt').exists()}")

        # Build a malicious archive whose member tries to climb out.
        evil = root / "evil.tar"
        with tarfile.open(evil, "w") as tf:
            payload = b"gotcha\n"
            info = tarfile.TarInfo("../outside.txt")
            info.size = len(payload)
            tf.addfile(info, io.BytesIO(payload))
        with tarfile.open(evil) as tf:
            try:
                tf.extractall(root / "safe", filter="data")
            except tarfile.FilterError as exc:
                # The message names the full temp path, so print just the type.
                print(f"'../outside.txt' blocked: {type(exc).__name__}")
        print(f"nothing written outside: {not (root / 'outside.txt').exists()}")


def main() -> None:
    gzip_demo()
    print()
    zipfile_demo()
    print()
    tarfile_demo()


if __name__ == "__main__":
    main()
