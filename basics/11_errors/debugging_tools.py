"""Debugging tools — reading tracebacks, inspecting the stack, and `breakpoint()`.

A traceback is a map of how the program got to the error. Read it from the
bottom up: the last line names the exception and its message, the frame just
above it is where it was raised, and each frame higher up is the caller of
the one below it. Most bugs are fixed by reading the bottom two or three
frames carefully.

    traceback.format_exc()   the current exception's traceback as a string
    traceback.print_exc()    the same, printed (to stderr unless file=...)
    inspect.stack()          the live call stack: who called this function?
    breakpoint()             stop here and open the debugger (pdb)
    f"{value=}"              a quick labelled print while investigating
    logging.debug(...)       debug output you can leave in and switch off

This file never actually opens pdb, because pdb waits for keyboard input.
"""

import inspect
import io
import os
import sys
import traceback
from typing import Any


HERE = os.path.dirname(os.path.abspath(__file__)) + os.sep


def parse_port(text: str) -> int:
    return int(text)  # fails for "eighty"


def load_config(settings: dict[str, str]) -> int:
    return parse_port(settings["port"])


def read_traceback_demo() -> None:
    try:
        load_config({"port": "eighty"})
    except ValueError:
        # format_exc() returns the traceback a crash would have printed.
        # The folder name is trimmed so the output is the same on any machine.
        print(traceback.format_exc().replace(HERE, ""))

    print("How to read it, bottom up:")
    print("  ValueError: ...           what went wrong")
    print("  in parse_port             where it was raised: int(text)")
    print("  in load_config            who called parse_port, and with what")
    print("  in read_traceback_demo    the outermost call, where we started")


def traceback_tools_demo() -> None:
    try:
        load_config({})  # a missing key this time
    except KeyError as exc:
        # print_exc writes to stderr by default; file= sends it anywhere.
        buffer = io.StringIO()
        traceback.print_exc(limit=1, file=buffer)  # limit: outermost frames only
        print("print_exc(limit=1):")
        print("  " + buffer.getvalue().replace(HERE, "").strip().replace("\n", "\n  "))

        # Just the last line, handy for a short log message.
        only = traceback.format_exception_only(exc)
        print(f"format_exception_only: {only[-1].strip()}")

        # The frames as data, for when you want to process them yourself.
        print("frames, oldest first:")
        for frame in traceback.extract_tb(exc.__traceback__):
            print(f"  {frame.name}() line {frame.lineno}: {frame.line}")


def who_called_me() -> str:
    """Describe the caller of whichever function calls this helper."""
    # stack()[0] is this helper, [1] the function asking, [2] its caller.
    stack = inspect.stack()
    me, caller = stack[1], stack[2]
    line = caller.code_context[0].strip() if caller.code_context else "?"
    return f"{me.function}() was called by {caller.function}(): {line}"


def save_user(name: str) -> None:
    print(f"  {who_called_me()}")


def signup() -> None:
    save_user("ada")


def inspect_stack_demo() -> None:
    print("inspect.stack():")
    signup()
    chain = [frame.function for frame in inspect.stack()[:3]]
    print(f"  current call chain, innermost first: {chain}")


PDB_COMMANDS = {
    "p expr": "print an expression, e.g. p total",
    "n": "next: run the current line, step over calls",
    "s": "step: go into the function called on this line",
    "c": "continue until the next breakpoint",
    "l": "list the source around the current line",
    "w": "where: print the stack, like a traceback",
    "q": "quit the debugger and the program",
}


def average(numbers: list[float]) -> float:
    total = sum(numbers)
    breakpoint()  # in real code: pause here and inspect total and numbers
    return total / len(numbers)


def breakpoint_demo() -> None:
    # breakpoint() simply calls sys.breakpointhook(), which starts pdb.
    # Setting PYTHONBREAKPOINT=0 turns every breakpoint() into a no-op.
    # Here we swap in a harmless hook to show what the debugger would see.
    def peek(*args: Any, **kwargs: Any) -> None:
        frame = sys._getframe(1)  # the function that called breakpoint()
        print(f"  paused in {frame.f_code.co_name}(), locals = {frame.f_locals}")

    print("breakpoint() with a stand-in hook:")
    original = sys.breakpointhook
    sys.breakpointhook = peek
    try:
        print(f"  average = {average([2.0, 4.0, 9.0])}")
    finally:
        sys.breakpointhook = original

    print("  pdb commands you will use most:")
    for command, meaning in PDB_COMMANDS.items():
        print(f"    {command:7} {meaning}")


def main() -> None:
    read_traceback_demo()
    print()
    traceback_tools_demo()
    print()
    inspect_stack_demo()
    print()
    breakpoint_demo()


if __name__ == "__main__":
    main()
