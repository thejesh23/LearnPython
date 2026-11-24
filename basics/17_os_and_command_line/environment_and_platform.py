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

import os


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


def main() -> None:
    environ_demo()


if __name__ == "__main__":
    main()
