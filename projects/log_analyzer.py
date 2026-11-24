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
import re
import statistics
import tempfile
from collections import Counter
from collections.abc import Iterable
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from pathlib import Path


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


# re.VERBOSE lets a long pattern be laid out and commented. In this mode
# spaces are ignored, so a literal space is written as [ ].
LINE = re.compile(
    r"""
    (?P<ip>\S+) [ ] \S+ [ ] \S+ [ ]          # client address, two unused fields
    \[ (?P<time>[^\]]+) \] [ ]               # [12/Mar/2024:10:00:03 +0000]
    " (?P<method>[A-Z]+) [ ] (?P<path>\S+) [ ] [^"]* " [ ]
    (?P<status>\d{3}) [ ] (?P<size>\d+) [ ]
    (?P<seconds>\d+\.\d+)
    $""",
    re.VERBOSE,
)


@dataclass(frozen=True)
class LogEntry:
    ip: str
    time: datetime
    method: str
    path: str
    status: int
    size: int
    seconds: float


def parse_line(line: str) -> LogEntry | None:
    """Return a LogEntry, or None if the line is not in the expected format."""
    m = LINE.match(line.strip())
    if m is None:
        return None
    return LogEntry(
        ip=m["ip"],
        time=datetime.strptime(m["time"], TIME_FORMAT),
        method=m["method"],
        path=m["path"],
        status=int(m["status"]),
        size=int(m["size"]),
        seconds=float(m["seconds"]),
    )


def parse_lines(lines: Iterable[str], rejected: list[str]) -> Iterator[LogEntry]:
    """Parse lazily, collecting bad lines instead of stopping at the first."""
    for line in lines:
        if not line.strip():
            continue
        entry = parse_line(line)
        if entry is None:
            rejected.append(line.rstrip("\n"))
        else:
            yield entry


def parse_demo() -> None:
    print("== stage 2: parsing ==")
    first = next(generate_log(1))
    entry = parse_line(first)
    print(f"line:  {first}")
    print(f"entry: {entry}")
    if entry:
        print(f"typed fields: {entry.status + 1 = }, {entry.time.minute = }")

    rejected: list[str] = []
    lines = [*generate_log(3), "garbage line", '1.2.3.4 - - [bad date] "GET /"']
    entries = list(parse_lines(lines, rejected))
    print(f"parsed {len(entries)} entries, rejected {rejected}")


@dataclass
class Stats:
    total: int
    statuses: Counter[int]
    per_minute: Counter[datetime]
    durations: dict[str, list[float]]
    bytes_sent: int


def analyze(entries: Iterable[LogEntry]) -> Stats:
    """One pass over the entries, filling every counter as we go."""
    stats = Stats(0, Counter(), Counter(), {}, 0)
    for e in entries:
        stats.total += 1
        stats.statuses[e.status] += 1
        # Round each time down to its minute so they can be counted together.
        stats.per_minute[e.time.replace(second=0)] += 1
        stats.durations.setdefault(e.path, []).append(e.seconds)
        stats.bytes_sent += e.size
    return stats


def slowest_paths(stats: Stats, n: int = 3) -> list[tuple[str, float, float]]:
    """(path, mean seconds, 95th percentile seconds), slowest mean first."""
    rows = []
    for path, times in stats.durations.items():
        # The 95th percentile: 95% of requests were faster than this. It
        # shows the slow tail that an average hides.
        p95 = statistics.quantiles(times, n=20)[-1] if len(times) > 1 else times[0]
        rows.append((path, statistics.mean(times), p95))
    return sorted(rows, key=lambda row: row[1], reverse=True)[:n]


def error_rate(stats: Stats) -> float:
    errors = sum(n for code, n in stats.statuses.items() if code >= 400)
    return errors / stats.total if stats.total else 0.0


def stats_demo() -> None:
    print("== stage 3: statistics ==")
    stats = analyze(parse_lines(generate_log(1000), []))
    print(f"requests: {stats.total}")
    print(f"status codes: {dict(sorted(stats.statuses.items()))}")
    print(f"error rate: {error_rate(stats):.1%}")
    for path, mean, p95 in slowest_paths(stats):
        print(f"slow: {path:<12} mean {mean:.3f}s  p95 {p95:.3f}s")
    minute, count = stats.per_minute.most_common(1)[0]
    print(f"busiest minute: {minute:%H:%M} with {count} requests")


def bar(count: int, biggest: int, width: int = 30) -> str:
    return "#" * max(1, round(count / biggest * width)) if count else ""


def format_report(stats: Stats, rejected: list[str]) -> str:
    lines = ["ACCESS LOG REPORT", "================="]
    first, last = min(stats.per_minute), max(stats.per_minute)
    lines += [
        f"period        {first:%Y-%m-%d %H:%M} to {last:%H:%M} UTC",
        f"requests      {stats.total:,}",
        f"bad lines     {len(rejected)}",
        f"data sent     {stats.bytes_sent / 1_000_000:.1f} MB",
        f"error rate    {error_rate(stats):.1%}",
        "",
        "Status codes",
    ]
    biggest = max(stats.statuses.values())
    for code, count in sorted(stats.statuses.items()):
        lines.append(f"  {code}  {count:>5}  {bar(count, biggest)}")

    lines += ["", "Slowest paths          mean     p95"]
    for path, mean, p95 in slowest_paths(stats, n=4):
        lines.append(f"  {path:<18} {mean:>6.3f}s {p95:>6.3f}s")

    lines += ["", "Requests per minute"]
    biggest = max(stats.per_minute.values())
    for minute, count in sorted(stats.per_minute.items()):
        lines.append(f"  {minute:%H:%M}  {count:>4}  {bar(count, biggest)}")
    return "\n".join(lines)


def analyze_file(path: Path) -> tuple[Stats, list[str]]:
    rejected: list[str] = []
    # Iterating over a file yields one line at a time, so even a log far
    # bigger than memory can be analyzed: nothing here keeps every line.
    with path.open(encoding="utf-8") as f:
        stats = analyze(parse_lines(f, rejected))
    return stats, rejected


def report_demo() -> None:
    print("== stage 4: the report ==")
    with tempfile.TemporaryDirectory() as tmp:
        log_file = Path(tmp) / "access.log"
        with log_file.open("w", encoding="utf-8") as f:
            for line in generate_log(1000):
                f.write(line + "\n")
            f.write("this line was cut off by a crash\n")  # real logs get messy
        print(f"wrote {log_file.name}: {log_file.stat().st_size:,} bytes")
        stats, rejected = analyze_file(log_file)
    print()
    print(format_report(stats, rejected))


def main() -> None:
    generate_demo()
    print()
    parse_demo()
    print()
    stats_demo()
    print()
    report_demo()


if __name__ == "__main__":
    main()
