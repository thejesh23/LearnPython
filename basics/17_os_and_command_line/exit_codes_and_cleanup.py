"""How a program ends: exit codes, stdout vs stderr, cleanup and signals.

When a program finishes it hands the operating system a small number, its
*exit code*. 0 means success; anything else means failure, and the number can
say which kind. Shells, CI systems and `subprocess` all read it: `make` stops,
a CI job turns red, `&&` skips the next command.

    falls off the end      exit code 0
    sys.exit()             0
    sys.exit(3)            3
    sys.exit("message")    prints the message to stderr, exit code 1
    uncaught exception     prints the traceback to stderr, exit code 1

A program has two output streams: stdout for results and stderr for errors
and progress. Keeping them apart lets `prog > out.txt` save the results while
the errors still show on screen.

`atexit` runs cleanup functions when the interpreter shuts down normally.
Signals are messages from the OS: pressing Ctrl+C sends SIGINT, which Python
turns into a KeyboardInterrupt exception.

Exit codes belong to a whole process, so the demos start small child
processes with `subprocess` and look at how they ended.
"""

import subprocess
import sys


def run_child(code: str) -> subprocess.CompletedProcess[str]:
    """Run a snippet of Python in a fresh process and capture how it ended."""
    return subprocess.run([sys.executable, "-c", code],
                          capture_output=True, text=True, timeout=30)


def exit_codes_demo() -> None:
    cases = [
        "print('all good')",
        "import sys; sys.exit()",
        "import sys; sys.exit(3)",
        "import sys; sys.exit('error: no input files')",
        "raise ValueError('bad value')",
    ]
    for code in cases:
        result = run_child(code)
        last_err = result.stderr.strip().splitlines()[-1:] or [""]
        print(f"{code:<45} -> exit {result.returncode}  stderr: {last_err[0]!r}")

    # sys.exit does not stop the program on the spot: it raises SystemExit.
    # That means finally blocks still run, and the exception can be caught.
    try:
        try:
            sys.exit(5)
        finally:
            print("finally ran before the exit")
    except SystemExit as exc:
        print(f"caught SystemExit with code {exc.code}, so we keep going")


TWO_STREAMS = """
import sys
print("result line 1")
print("warning: skipped a bad row", file=sys.stderr)
print("result line 2")
"""


def streams_demo() -> None:
    result = run_child(TWO_STREAMS)
    # The two streams arrive separately, like `prog > results.txt` would see.
    print(f"stdout: {result.stdout.splitlines()}")
    print(f"stderr: {result.stderr.splitlines()}")

    # stderr=subprocess.STDOUT merges them into one stream, like `2>&1`.
    merged = subprocess.run([sys.executable, "-c", TWO_STREAMS],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True)
    print(f"merged: {len(merged.stdout.splitlines())} lines in one stream")
    # In your own code: print(..., file=sys.stderr) for messages that are not
    # the program's result. The logging module writes to stderr by default.


ATEXIT_CHILD = """
import atexit, os, sys

def close_db(): print("  closing the database")
def remove_lock(): print("  removing the lock file")

atexit.register(close_db)
atexit.register(remove_lock)   # registered last, so it runs first
print("  working")
{ending}
"""


def atexit_demo() -> None:
    endings = {
        "normal end": "",
        "sys.exit(2)": "sys.exit(2)",
        "uncaught error": "raise RuntimeError('boom')",
        # os._exit ends the process immediately: no atexit, no finally,
        # and unflushed output is lost. Only for special cases.
        "os._exit(4)": "sys.stdout.flush(); os._exit(4)",
    }
    for label, ending in endings.items():
        result = run_child(ATEXIT_CHILD.replace("{ending}", ending))
        print(f"{label} (exit code {result.returncode}):")
        print(result.stdout.rstrip())


def main() -> None:
    exit_codes_demo()
    print()
    streams_demo()
    print()
    atexit_demo()


if __name__ == "__main__":
    main()
