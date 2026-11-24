"""Practice: data and storage (chapter 18).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch18_data_and_storage.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch18_data_and_storage.py: try first, peek second. The
lessons for this chapter are in basics/18_data_and_storage/.
"""

import hashlib
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any


def verdict(error: BaseException) -> str:
    """Turn the exception a test raised into a short status."""
    # A stub raises NotImplementedError. Other errors may wrap it, so follow
    # the chain of causes (and look inside exception groups) before deciding.
    link: BaseException | None = error
    for _ in range(20):
        if link is None:
            break
        if isinstance(link, NotImplementedError):
            return "[todo] not attempted"
        if isinstance(link, BaseExceptionGroup) and link.subgroup(
            NotImplementedError
        ):
            return "[todo] not attempted"
        link = link.__cause__ or link.__context__
    if isinstance(error, AssertionError):
        return f"[not yet] {str(error) or 'a check failed'}"
    return f"[not yet] {type(error).__name__}: {error}"


def report(title: str, test: Callable[[Any], None], impl: Any) -> None:
    """Run one test against one implementation and print a one-line status."""
    try:
        test(impl)
        status = "[solved]"
    except KeyboardInterrupt:
        raise
    except BaseException as error:  # never crash: one line per exercise
        status = verdict(error)
    print(f"{title:<40} {status}")


# --- Exercise 1 -------------------------------------------------------------

def sha256_file(path: Path) -> str:
    """Return the SHA-256 fingerprint of a file as 64 hex characters.

    This is how download pages let you check a file arrived intact. Open
    the file in binary mode ("rb") and feed it to hashlib.sha256() in
    chunks of, say, 64 KiB with .update(), so even a huge file never has
    to fit in memory. Finish with .hexdigest().
    """
    raise NotImplementedError


def test_sha256_file(impl: Callable[[Path], str]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "data.bin"
        path.write_bytes(b"")
        empty = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        got = impl(path)
        assert got == empty, f"an empty file should hash to {empty}, got {got}"
        path.write_bytes(b"abc")
        abc = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        got = impl(path)
        assert got == abc, f"b'abc' should hash to {abc}, got {got}"
        # Bigger than one chunk, with every byte value, so text mode would break.
        data = bytes(range(256)) * 1500
        path.write_bytes(data)
        want = hashlib.sha256(data).hexdigest()
        got = impl(path)
        assert got == want, f"a 384 KB file: expected {want}, got {got}"


def check_sha256_file() -> None:
    report("1. sha256_file", test_sha256_file, sha256_file)


def main() -> None:
    check_sha256_file()


if __name__ == "__main__":
    main()
