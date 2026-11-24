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


def main() -> None:
    run_demo()


if __name__ == "__main__":
    main()
