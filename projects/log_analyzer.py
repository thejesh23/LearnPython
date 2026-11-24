"""Web server log analyzer: turn thousands of log lines into a short report.

Every request a web server handles becomes one line in its access log. You
build the tool that answers the usual questions about such a log: how many
requests failed, which pages are slow, when was traffic busiest.

To keep the example self-contained, stage 1 *generates* a realistic log with
a seeded random number generator, so every run produces the same log and the
same report. The line format is the common "access log" layout with the
response time in seconds added at the end:

    203.0.113.42 - - [12/Mar/2024:10:00:03 +0000] "GET /cart HTTP/1.1" 200 5123 0.081

The IP addresses come from 203.0.113.0/24, a range reserved for examples.

Uses:
    04_strings             f-string alignment, padding and number formats
    07_collections         dicts of lists, sorting with key functions
    08_iterators           generators that produce and consume lines lazily
    09_classes             frozen dataclasses for parsed records
    12_modules_io          writing and reading a log file line by line
    13_standard_library    random, re (named groups, VERBOSE), datetime,
                           collections.Counter, statistics
"""

import random
from collections.abc import Iterator
from datetime import datetime
from datetime import timedelta
from datetime import timezone


# path: (how often it is requested, typical response time in seconds)
PATHS = {
    "/": (30, 0.02),
    "/static/app.js": (15, 0.005),
    "/products": (20, 0.08),
    "/api/search": (15, 0.35),
    "/cart": (10, 0.06),
    "/checkout": (5, 0.9),
    "/admin": (2, 0.03),
    "/old-page": (3, 0.01),
}
CLIENTS = [f"203.0.113.{n}" for n in (4, 17, 23, 42, 88, 101, 150)]
START = datetime(2024, 3, 12, 10, 0, 0, tzinfo=timezone.utc)
TIME_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


def pick_status(path: str, rng: random.Random) -> int:
    if path == "/old-page":
        return 404  # someone still links to a page that was removed
    if path == "/admin":
        return 403
    if path in ("/api/search", "/checkout") and rng.random() < 0.04:
        return 500  # the slow, complicated endpoints fail now and then
    return 200


def generate_log(count: int, seed: int = 2024) -> Iterator[str]:
    """Yield `count` log lines. The same seed always gives the same lines."""
    rng = random.Random(seed)  # our own generator, not the shared global one
    paths = list(PATHS)
    weights = [PATHS[p][0] for p in paths]
    now = START
    for _ in range(count):
        # Requests arrive at random; a sale between 10:04 and 10:06 brings
        # four times the traffic, so there is a peak to find later.
        busy = 4 <= now.minute < 6
        now += timedelta(seconds=rng.expovariate(4.0 if busy else 1.0))
        path = rng.choices(paths, weights)[0]
        method = "POST" if path == "/checkout" else "GET"
        status = pick_status(path, rng)
        size = rng.randint(200, 20_000) if status == 200 else rng.randint(150, 600)
        seconds = rng.expovariate(1 / PATHS[path][1])
        stamp = now.strftime(TIME_FORMAT)
        yield (
            f'{rng.choice(CLIENTS)} - - [{stamp}] "{method} {path} HTTP/1.1" '
            f"{status} {size} {seconds:.3f}"
        )


def generate_demo() -> None:
    print("== stage 1: generating a log ==")
    lines = list(generate_log(5))
    for line in lines:
        print(f"  {line}")
    print(f"same seed, same log: {lines == list(generate_log(5))}")
    print(f"other seed, other log: {lines != list(generate_log(5, seed=1))}")


def main() -> None:
    generate_demo()


if __name__ == "__main__":
    main()
