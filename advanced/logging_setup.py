"""`logging` — levels, handlers, and why `print` does not scale.

The model has four parts: a **logger** (named, hierarchical) creates records, a
**handler** decides where they go, a **formatter** decides how they look, and a
**filter** can drop them. Libraries create loggers and nothing else;
applications configure handlers. That separation is why a library must never
call `basicConfig`.

Use `logger.exception(...)` inside an `except` block: it logs at ERROR *and*
attaches the traceback. And pass arguments lazily — `logger.info("x=%s", x)`
formats only if the message is actually emitted.
"""

import logging
import sys


class RequestFilter(logging.Filter):
    """Attach contextual data to every record passing through."""

    def __init__(self, request_id: str) -> None:
        super().__init__()
        self.request_id = request_id

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = self.request_id
        return True


def configure() -> logging.Logger:
    logger = logging.getLogger("demo")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)  # a handler can be stricter than the logger
    console.setFormatter(
        logging.Formatter("  %(levelname)-8s %(name)s [%(request_id)s] %(message)s")
    )
    console.addFilter(RequestFilter("req-42"))
    logger.addHandler(console)
    return logger


def main() -> None:
    logger = configure()

    logger.debug("not shown: the handler's level is INFO")
    logger.info("processing %d items", 3)  # lazy formatting
    logger.warning("disk at %d%%", 91)
    logger.error("failed to reach %s", "db.internal")

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("computation failed")  # ERROR + traceback

    # Loggers are hierarchical: "demo.db" inherits demo's handlers.
    child = logging.getLogger("demo.db")
    child.info("child logger propagates to the parent's handler")
    print(f"child level inherited: {child.getEffectiveLevel()} "
          f"(= {logging.getLevelName(child.getEffectiveLevel())})")

    # Per-call context without a filter.
    logger.info("with extra", extra={"request_id": "req-99"})

    # Levels are just integers, so comparisons work as expected.
    print(f"levels: DEBUG={logging.DEBUG} INFO={logging.INFO} "
          f"WARNING={logging.WARNING} ERROR={logging.ERROR} CRITICAL={logging.CRITICAL}")
    print("libraries: getLogger(__name__) and nothing else; apps configure handlers")


if __name__ == "__main__":
    main()
