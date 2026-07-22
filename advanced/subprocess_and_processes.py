"""`subprocess` — running other programs safely.

One rule dominates: pass a **list of arguments**, not a string with
`shell=True`. With a list, the arguments go straight to `execve` and a filename
containing `; rm -rf ~` is just an odd filename. With `shell=True` it is code.

`subprocess.run` is the modern entry point: it waits, captures output when
asked, and `check=True` turns a non-zero exit into a `CalledProcessError`
carrying the return code and the captured streams.

For long-running children use `Popen` and stream their output; for anything
that might hang, always pass a timeout.
"""

import subprocess
import sys


def main() -> None:
    print("run with captured output:")
    result = subprocess.run(
        [sys.executable, "-c", "print('hello from a child process')"],
        capture_output=True,
        text=True,
        check=True,
    )
    print(f"  stdout: {result.stdout.strip()!r}")
    print(f"  returncode: {result.returncode}")

    print("non-zero exit with check=True raises:")
    try:
        subprocess.run(
            [sys.executable, "-c", "import sys; sys.stderr.write('bad input\\n'); sys.exit(3)"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"  CalledProcessError: exit {exc.returncode}, stderr {exc.stderr.strip()!r}")

    print("timeouts stop a hung child:")
    try:
        subprocess.run([sys.executable, "-c", "import time; time.sleep(30)"], timeout=0.2)
    except subprocess.TimeoutExpired as exc:
        print(f"  TimeoutExpired after {exc.timeout}s — the child was killed")

    print("feeding stdin:")
    piped = subprocess.run(
        [sys.executable, "-c", "import sys; print(sys.stdin.read().upper(), end='')"],
        input="shout this\n",
        capture_output=True,
        text=True,
    )
    print(f"  {piped.stdout.strip()!r}")

    print("streaming a long-running child with Popen:")
    proc = subprocess.Popen(
        [sys.executable, "-u", "-c", "for i in range(3): print('tick', i)"],
        stdout=subprocess.PIPE,
        text=True,
    )
    for line in proc.stdout:
        print(f"  child said: {line.rstrip()}")
    proc.wait()
    print(f"  exited with {proc.returncode}")

    print("argument lists are injection-proof:")
    hostile = "file.txt; echo pwned"
    safe = subprocess.run(
        [sys.executable, "-c", "import sys; print('argument received:', sys.argv[1])", hostile],
        capture_output=True,
        text=True,
    )
    print(f"  {safe.stdout.strip()}")
    print("  the same string with shell=True would have executed the echo")

    print("environment and working directory are explicit:")
    env_result = subprocess.run(
        [sys.executable, "-c", "import os; print(os.environ.get('DEMO_VAR'))"],
        capture_output=True,
        text=True,
        env={"DEMO_VAR": "set-for-child", "PATH": ""},
    )
    print(f"  child saw DEMO_VAR={env_result.stdout.strip()}")


if __name__ == "__main__":
    main()
