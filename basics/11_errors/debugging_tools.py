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

import os
import traceback


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


def main() -> None:
    read_traceback_demo()


if __name__ == "__main__":
    main()
