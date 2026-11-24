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


def named_loggers_demo() -> None:
    # getLogger(__name__) is the usual pattern: the name shows where a
    # message came from. Dots form a hierarchy: "app.db" is a child of "app".
    fmt = logging.Formatter("%(name)-8s %(levelname)-8s %(message)s")
    for handler in logging.getLogger().handlers:
        handler.setFormatter(fmt)

    db = logging.getLogger("app.db")
    web = logging.getLogger("app.web")
    db.info("connected")
    web.info("listening on port 8000")

    # Quieten one noisy part without touching the rest.
    db.setLevel(logging.WARNING)
    db.info("query took 3 ms (now hidden)")
    db.warning("slow query: 2.4 s")
    web.info("still visible")


def main() -> None:
    levels_demo()
    print()
    named_loggers_demo()


if __name__ == "__main__":
    main()
