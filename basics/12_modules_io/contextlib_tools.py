"""`contextlib` — ready-made context managers for everyday jobs.

context_managers.py shows how to write your own and covers `suppress`. The
rest of the module has several small tools that save you from writing one:

    ExitStack        enter any number of context managers, chosen at runtime
    redirect_stdout  send print() output somewhere else for a while
    closing          give `with` to an object that only has a .close() method
    nullcontext      a do-nothing stand-in when a `with` is optional
    chdir            change the working directory and change it back (3.11+)

Each one guarantees its cleanup runs however the block ends, which is the
whole point of `with`.
"""

import io
import os
import sys
import tempfile
from contextlib import AbstractContextManager, nullcontext
from contextlib import ExitStack
from contextlib import chdir
from contextlib import closing
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import IO


def merge_files(paths: list[Path]) -> str:
    # `with open(a) as f1, open(b) as f2:` needs the count written in the
    # code. ExitStack takes them one by one and closes all of them, newest
    # first, when the block ends.
    with ExitStack() as stack:
        files = [stack.enter_context(p.open(encoding="utf-8")) for p in paths]
        stack.callback(print, f"  closing {len(files)} files")  # any cleanup
        return " + ".join(f.read().strip() for f in files)


def exit_stack_demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        for name in ("a", "b", "c"):
            path = Path(tmp) / f"{name}.txt"
            path.write_text(f"part {name}\n", encoding="utf-8")
            paths.append(path)
        print(f"merged: {merge_files(paths)}")


def chatty_report() -> int:
    """Prints instead of returning text: common in older or quick code."""
    print("line 1 of the report")
    print("line 2 of the report")
    return 2


def redirect_demo() -> None:
    buffer = io.StringIO()
    with redirect_stdout(buffer):  # print() now writes into the buffer
        lines = chatty_report()
    captured = buffer.getvalue()
    print(f"captured {lines} lines: {captured.splitlines()}")

    # redirect_stderr works the same way for error output.
    errors = io.StringIO()
    with redirect_stderr(errors):
        print("something went wrong", file=sys.stderr)
    print(f"captured stderr: {errors.getvalue().strip()!r}")
    # Only Python-level writes are redirected; output from a subprocess or a
    # C library goes straight to the real stdout.


class LegacyClient:
    """Has close() but no __enter__/__exit__, so `with` would fail."""

    def __init__(self) -> None:
        self.closed = False

    def fetch(self) -> str:
        if self.closed:
            raise RuntimeError("client is closed")
        return "data"

    def close(self) -> None:
        self.closed = True


def closing_demo() -> None:
    try:
        with LegacyClient():  # type: ignore[attr-defined]
            pass
    except TypeError as exc:
        print(f"plain with: TypeError: {exc}")

    # closing(x) calls x.close() at the end of the block, even on an error.
    with closing(LegacyClient()) as client:
        print(f"fetched {client.fetch()!r}")
    print(f"closed afterwards: {client.closed}")


def write_report(lines: list[str], out: IO[str] | None, folder: Path) -> Path | None:
    # Either open (and later close) a file we own, or use the stream we were
    # given and leave it open. nullcontext(x) yields x and does nothing else,
    # so one `with` statement handles both cases.
    target = folder / "report.txt"
    manager: AbstractContextManager[IO[str]]
    if out is None:
        manager = target.open("w", encoding="utf-8")
    else:
        manager = nullcontext(out)
    with manager as f:
        for line in lines:
            f.write(line + "\n")
    return target if out is None else None


def nullcontext_demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        written = write_report(["a", "b"], None, Path(tmp))
        if written:
            print(f"own file: {written.read_text(encoding='utf-8').split()}")

        stream = io.StringIO()
        write_report(["c", "d"], stream, Path(tmp))
        print(f"caller's stream still open: {not stream.closed}, "
              f"holds {stream.getvalue().split()}")


def chdir_demo() -> None:
    start = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        with chdir(tmp):
            # Relative paths now resolve inside tmp.
            Path("notes.txt").write_text("hi", encoding="utf-8")
            print(f"inside: wrote notes.txt, listing = {os.listdir('.')}")
            print(f"cwd is the temp folder: {Path.cwd() == Path(tmp).resolve()}")
        print(f"back where we started: {os.getcwd() == start}")
    # The working directory is shared by the whole process, so avoid chdir
    # in threaded code; pass full paths instead when you can.


def main() -> None:
    exit_stack_demo()
    print()
    redirect_demo()
    print()
    closing_demo()
    print()
    nullcontext_demo()
    print()
    chdir_demo()


if __name__ == "__main__":
    main()
