"""Running other programs from Python with `subprocess.run`.

A Python script often needs to start another program: git, a compiler, a
converter, or another Python script. `subprocess.run` starts it, waits for it
to finish and hands back a `CompletedProcess` with its exit code and, when
asked, its output.

    capture_output=True   collect stdout and stderr instead of printing them
    text=True             give back str instead of bytes
    check=True            raise CalledProcessError if the exit code is not 0
    timeout=seconds       raise TimeoutExpired if it takes too long

Pass the command as a *list*: the program name, then each argument as its own
item. Do not build one string and use `shell=True`, especially with anything a
user typed: the shell treats characters like ; and | as instructions.

The examples run `sys.executable -c "..."`, which is the same Python that runs
this file, so they work on every operating system.
"""

import subprocess
import sys


def run_demo() -> None:
    # The command is a list: program first, then one item per argument.
    command = [sys.executable, "-c", "print('hello from a child process')"]
    result = subprocess.run(command, capture_output=True, text=True)
    print(f"returncode: {result.returncode}")
    print(f"stdout: {result.stdout!r}")  # note the trailing newline
    print(f"stderr: {result.stderr!r}")

    # Arguments after the code show up in the child's sys.argv.
    code = "import sys; print(sum(int(a) for a in sys.argv[1:]))"
    result = subprocess.run([sys.executable, "-c", code, "2", "3", "4"],
                            capture_output=True, text=True)
    print(f"child added 2 + 3 + 4 = {result.stdout.strip()}")

    # Without text=True the output is bytes.
    raw = subprocess.run([sys.executable, "-c", "print('hi')"], capture_output=True)
    print(f"without text=True: {raw.stdout!r}")

    # input= feeds text to the child's standard input.
    upper = subprocess.run([sys.executable, "-c", "print(input().upper())"],
                           input="shout this\n", capture_output=True, text=True)
    print(f"input= -> {upper.stdout.strip()}")


FAILING = "import sys; print('working...'); sys.exit('config file is missing')"


def check_demo() -> None:
    # By default a failing program is not an error in Python: you must look
    # at returncode yourself, and it is easy to forget.
    result = subprocess.run([sys.executable, "-c", FAILING],
                            capture_output=True, text=True)
    print(f"without check: returncode={result.returncode}, no exception raised")

    # check=True turns a non-zero exit code into an exception.
    try:
        subprocess.run([sys.executable, "-c", FAILING],
                       capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"CalledProcessError: exit code {exc.returncode}")
        print(f"  its stdout: {exc.stdout.strip()!r}")
        print(f"  its stderr: {exc.stderr.strip()!r}")

    # A program that does not exist fails before it even starts.
    try:
        subprocess.run(["surely-not-a-real-program"], capture_output=True)
    except FileNotFoundError:
        print("unknown program -> FileNotFoundError")


def timeout_demo() -> None:
    # Anything that talks to a network or a user can hang. A timeout stops
    # the child and raises TimeoutExpired instead of waiting forever.
    sleeper = [sys.executable, "-c", "import time; time.sleep(10)"]
    try:
        subprocess.run(sleeper, capture_output=True, timeout=0.5)
    except subprocess.TimeoutExpired as exc:
        print(f"TimeoutExpired after {exc.timeout} seconds; the child was killed")

    quick = subprocess.run([sys.executable, "-c", "print('done')"],
                           capture_output=True, text=True, timeout=30)
    print(f"a fast program finishes normally: {quick.stdout.strip()!r}")


def main() -> None:
    run_demo()
    print()
    check_demo()
    print()
    timeout_demo()


if __name__ == "__main__":
    main()
