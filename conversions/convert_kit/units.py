"""A unit converter built from one table per quantity.

Each unit is stored as a pair of functions to and from a base unit, so any
pair of units converts through the base: n units need 2n functions, not n².
Linear units (bytes, seconds, metres) are just a scale factor; temperature
needs an offset too, which is why every entry is a pair of functions.
"""

from collections.abc import Callable

Pair = tuple[Callable[[float], float], Callable[[float], float]]


def _scale(factor: float) -> Pair:
    return (lambda v: v * factor, lambda v: v / factor)


UNITS: dict[str, dict[str, Pair]] = {
    "temperature": {
        "C": (lambda v: v, lambda v: v),
        "F": (lambda v: (v - 32) * 5 / 9, lambda v: v * 9 / 5 + 32),
        "K": (lambda v: v - 273.15, lambda v: v + 273.15),
        "R": (lambda v: (v - 491.67) * 5 / 9, lambda v: (v + 273.15) * 9 / 5),
    },
    "data": {
        "B": _scale(1), "kB": _scale(1e3), "MB": _scale(1e6), "GB": _scale(1e9),
        "KiB": _scale(2**10), "MiB": _scale(2**20), "GiB": _scale(2**30),
    },
    "time": {
        "s": _scale(1), "min": _scale(60), "h": _scale(3600), "d": _scale(86_400),
        "week": _scale(604_800),
    },
    "length": {
        "m": _scale(1), "km": _scale(1000), "cm": _scale(0.01), "in": _scale(0.0254),
        "ft": _scale(0.3048), "mi": _scale(1609.344),
    },
}


def quantity_of(unit: str) -> str:
    for quantity, table in UNITS.items():
        if unit in table:
            return quantity
    raise KeyError(f"unknown unit: {unit!r}")


def convert(value: float, source: str, target: str) -> float:
    """convert(100, 'C', 'F') -> 212.0; units must measure the same quantity."""
    quantity = quantity_of(source)
    if quantity_of(target) != quantity:
        raise ValueError(f"cannot convert {source} ({quantity}) to {target}")
    to_base, _ = UNITS[quantity][source]
    _, from_base = UNITS[quantity][target]
    base = to_base(value)
    if quantity == "temperature" and base < -273.15 - 1e-9:
        raise ValueError(f"{value} {source} is below absolute zero")
    return from_base(base)


def humanize_bytes(n: int, si: bool = False) -> str:
    """1536 -> '1.5 KiB' (or '1.5 kB' with si=True); rounds before promoting."""
    base = 1000 if si else 1024
    names = ["B", "kB", "MB", "GB", "TB"] if si else ["B", "KiB", "MiB", "GiB", "TiB"]
    if abs(n) < base:
        return f"{n} B"
    value, i = float(n), 0
    while i < len(names) - 1 and abs(round(value, 1)) >= base:
        value /= base
        i += 1
    return f"{value:.1f} {names[i]}"


def clock(seconds: int) -> str:
    """3661 -> '1:01:01'; hours are not wrapped at 24."""
    sign = "-" if seconds < 0 else ""
    minutes, secs = divmod(abs(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{sign}{hours}:{minutes:02}:{secs:02}"
    return f"{sign}{minutes}:{secs:02}"
