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
import sys
import tempfile
from contextlib import ExitStack
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


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


def main() -> None:
    exit_stack_demo()
    print()
    redirect_demo()


if __name__ == "__main__":
    main()
