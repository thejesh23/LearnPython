"""`logging` — messages with levels, sources and timestamps, instead of print.

print() always prints. A log call has a *level*, and the program decides at
one central place which levels to show and where they go:

    DEBUG < INFO < WARNING < ERROR < CRITICAL

Libraries create a logger named after their module and simply log; the
application configures handlers once at startup. Here everything goes to
standard output so the demo is easy to read; the default is standard error.
"""

import logging
import sys


def levels_demo() -> None:
    # basicConfig sets up the root logger; force=True replaces earlier setup.
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, force=True,
                        format="%(levelname)-8s %(message)s")
    logging.debug("hidden: DEBUG is below the INFO threshold")
    logging.info("server starting")
    logging.warning("disk 85% full")
    logging.error("could not open config file")

    # Lowering the threshold reveals the debug messages.
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("now visible")


def main() -> None:
    levels_demo()


if __name__ == "__main__":
    main()
