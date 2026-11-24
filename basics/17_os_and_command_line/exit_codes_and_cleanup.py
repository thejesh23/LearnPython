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


def main() -> None:
    exit_codes_demo()


if __name__ == "__main__":
    main()
