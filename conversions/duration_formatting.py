"""Seconds to clock strings and back, plus a compact "2h 5m" form.

Formatting is repeated divmod: seconds into minutes and seconds, minutes into
hours and minutes. Hours are not wrapped at 24, because a 30-hour video is
30:00:00, not 6:00:00. Parsing runs Horner's method in base 60 over the colon
groups, the same trick used for any positional number, so "1:02:03" is
(1 * 60 + 2) * 60 + 3.

The compact form drops zero units and is what you see in "uploaded 3d 4h ago".
datetime.timedelta does some of this, but its str() wraps at days ("1 day,
6:00:00"), which is a useful contrast.
"""

from datetime import timedelta

UNITS = [("d", 86_400), ("h", 3_600), ("m", 60), ("s", 1)]


def to_clock(total: int) -> str:
    sign = "-" if total < 0 else ""
    minutes, seconds = divmod(abs(total), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{sign}{hours}:{minutes:02}:{seconds:02}"
    return f"{sign}{minutes}:{seconds:02}"


def from_clock(text: str) -> int:
    sign = -1 if text.startswith("-") else 1
    parts = text.lstrip("-").split(":")
    if not 1 <= len(parts) <= 3 or not all(p.isdigit() for p in parts):
        raise ValueError(f"bad clock string: {text!r}")
    if any(int(p) >= 60 for p in parts[1:]):
        raise ValueError(f"minutes and seconds must be under 60: {text!r}")
    total = 0
    for part in parts:
        total = total * 60 + int(part)
    return sign * total


def to_compact(total: int, max_units: int = 2) -> str:
    if total == 0:
        return "0s"
    pieces: list[str] = []
    rest = abs(total)
    for name, size in UNITS:
        count, rest = divmod(rest, size)
        if count:
            pieces.append(f"{count}{name}")
    return ("-" if total < 0 else "") + " ".join(pieces[:max_units])


def main() -> None:
    for n in [0, 5, 59, 60, 61, 3599, 3600, 3661, 86_399, 108_000, -75]:
        print(f"{n:>7} -> {to_clock(n):>9}   {to_compact(n):>7}   "
              f"timedelta: {timedelta(seconds=n)}")

    print()
    for text in ["1:02:03", "45", "2:30", "30:00:00", "-1:15"]:
        print(f"{text!r:>12} -> {from_clock(text)} s")

    ok = all(from_clock(to_clock(n)) == n for n in range(-5000, 200_000, 37))
    print(f"\nround trip across a sweep: {ok}")
    print(f"compact with three units: {to_compact(266_461, max_units=3)}")

    for bad in ["1:75", "a:b", "1:2:3:4"]:
        try:
            from_clock(bad)
        except ValueError as err:
            print(f"rejected: {err}")


if __name__ == "__main__":
    main()
