"""Solutions: data and storage (chapter 18).

Worked answers for exercises/ch18_data_and_storage.py. Try each exercise
yourself before reading its solution; the struggle is where the learning
happens.

This file reuses the test functions from the exercise file, so running it
checks these solutions exactly the way your own code is checked:

    python exercises/solutions/ch18_data_and_storage.py

Every line should say [solved]. Your answer does not need to match these
line by line; if the tests pass, it is a valid solution.
"""

import hashlib
import runpy
from pathlib import Path


# Run the exercise file as a module (its main() does not run) to reuse its
# report() helper and test_... functions.
EXERCISES = runpy.run_path(
    str(Path(__file__).resolve().parent.parent / "ch18_data_and_storage.py")
)
report = EXERCISES["report"]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        # iter(callable, sentinel) calls f.read(65536) until it returns b"".
        for chunk in iter(lambda: f.read(64 * 1024), b""):
            digest.update(chunk)
    # Since Python 3.11, hashlib.file_digest(f, "sha256") does this loop for you.
    return digest.hexdigest()


def check_sha256_file() -> None:
    report("1. sha256_file", EXERCISES["test_sha256_file"], sha256_file)


def main() -> None:
    check_sha256_file()


if __name__ == "__main__":
    main()
