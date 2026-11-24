"""Environment variables, the running Python, the current directory and PATH.

Every process inherits a set of *environment variables* from whatever started
it: a shell, an IDE, a CI job. They are the usual way to hand a program
settings that differ between machines (a log level, a database URL, an API key)
without editing code. In Python they live in `os.environ`, a dict-like mapping
of strings to strings.

The `sys` and `platform` modules describe the interpreter itself: which
version, which operating system, and which executable is running. The current
working directory decides what relative paths like "data.txt" mean. PATH is
the environment variable the operating system searches when you type a
command name without a folder in front of it.

This file prints only harmless facts. Environments often hold secrets, so it
never dumps the whole of `os.environ`.
"""

import contextlib
import os
import platform
import sys
import tempfile
from pathlib import Path


def env_int(name: str, default: int) -> int:
    """Read an integer setting; everything in os.environ is a string."""
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        raise ValueError(f"{name} must be a whole number, got {raw!r}") from None


def env_flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def environ_demo() -> None:
    # .get with a default never raises; os.environ["NAME"] raises KeyError.
    print(f"LEARNPY_LEVEL: {os.environ.get('LEARNPY_LEVEL', 'not set')}")
    try:
        os.environ["LEARNPY_LEVEL"]
    except KeyError:
        print("os.environ['LEARNPY_LEVEL'] -> KeyError")

    # Checking presence is safe to print; the values themselves may be secret.
    for name in ("HOME", "USERPROFILE", "PATH"):
        print(f"{name} is set: {name in os.environ}")

    # Setting a variable affects this process and programs it starts later.
    os.environ["LEARNPY_WORKERS"] = "4"
    os.environ["LEARNPY_DEBUG"] = "yes"
    print(f"workers: {env_int('LEARNPY_WORKERS', 1)} (an int, not '4')")
    print(f"debug:   {env_flag('LEARNPY_DEBUG')}")
    print(f"retries: {env_int('LEARNPY_RETRIES', 3)} (default used)")

    os.environ["LEARNPY_WORKERS"] = "four"
    try:
        env_int("LEARNPY_WORKERS", 1)
    except ValueError as exc:
        print(f"ValueError: {exc}")
    # pop removes it again; the shell that started us never saw any of this.
    for name in ("LEARNPY_WORKERS", "LEARNPY_DEBUG"):
        os.environ.pop(name)


def interpreter_demo() -> None:
    # version_info is a tuple, so comparisons just work.
    v = sys.version_info
    print(f"Python {v.major}.{v.minor}.{v.micro}")
    print(f"at least 3.12: {sys.version_info >= (3, 12)}")
    print(f"implementation: {platform.python_implementation()}")

    # sys.platform is fixed when Python is built: 'linux', 'darwin', 'win32'.
    # platform.system() asks the OS at run time: 'Linux', 'Darwin', 'Windows'.
    print(f"sys.platform: {sys.platform}, platform.system(): {platform.system()}")
    # os.name is 'posix' (Linux, macOS) or 'nt' (Windows): handy for branching.
    print(f"os.name: {os.name}")

    # The full path to the running interpreter. Use it to start another Python
    # that has the same packages as this one (see running_programs.py).
    exe = Path(sys.executable)
    print(f"sys.executable ends in: {exe.name}, absolute: {exe.is_absolute()}")
    # A virtual environment makes sys.prefix differ from sys.base_prefix.
    print(f"inside a virtual environment: {sys.prefix != sys.base_prefix}")


def cwd_demo() -> None:
    # The cwd is wherever the program was started from, not where the .py
    # file lives. Relative paths are resolved against it.
    start = Path.cwd()
    print(f"os.getcwd() == Path.cwd(): {os.getcwd() == str(start)}")
    inside = Path("data.txt").resolve().parent == start
    print(f"'data.txt' resolves to a file in the cwd: {inside}")
    here = Path(__file__).resolve().parent
    print(f"this script's own folder is the cwd: {here == start}")

    # contextlib.chdir (3.11+) changes the cwd and restores it afterwards.
    with tempfile.TemporaryDirectory() as folder:
        with contextlib.chdir(folder):
            Path("note.txt").write_text("hi", encoding="utf-8")  # a relative path
            print(f"inside chdir, note.txt exists: {Path('note.txt').exists()}")
        print(f"after the block, back where we started: {Path.cwd() == start}")
        landed = (Path(folder) / "note.txt").exists()
        print(f"the file landed in the temp folder: {landed}")
    # To find files that ship with your script, build paths from __file__.


def main() -> None:
    environ_demo()
    print()
    interpreter_demo()
    print()
    cwd_demo()


if __name__ == "__main__":
    main()
