"""Examples and self-check: python3 -m conversions.convert_kit"""

import random
import sys

from . import (
    UNITS,
    clock,
    convert,
    from_base,
    from_roman,
    humanize_bytes,
    to_base,
    to_roman,
    to_words,
)


def examples() -> None:
    print(f"1. 100 C = {convert(100, 'C', 'F'):g} F = {convert(100, 'C', 'K'):g} K")
    print(f"2. 500 GB = {convert(500, 'GB', 'GiB'):.1f} GiB, "
          f"humanized {humanize_bytes(500 * 10**9)}")
    print(f"3. 26.2 mi = {convert(26.2, 'mi', 'km'):.2f} km; 1 week = "
          f"{convert(1, 'week', 'h'):g} h; 3661 s = {clock(3661)}")
    print(f"4. 1994 = {to_roman(1994)}; MMXXIV = {from_roman('MMXXIV')}")
    print(f"5. 2,147,483,647 = {to_words(2_147_483_647)}")
    print(f"6. 255 = {to_base(255, 2)} (2) = {to_base(255, 16)} (16) "
          f"= {to_base(255, 36)} (36)")
    try:
        convert(1, "kB", "km")
    except ValueError as err:
        print(f"7. refused: {err}")


def self_check() -> None:
    rng = random.Random(4)
    for quantity, table in UNITS.items():
        for a in table:
            for b in table:
                v = rng.uniform(0, 1000)
                back = convert(convert(v, a, b), b, a)
                assert abs(back - v) < 1e-9 * max(1, v), (quantity, a, b)
    assert convert(-40, "C", "F") == -40 and convert(0, "K", "C") == -273.15
    for n in range(1, 4000):
        assert from_roman(to_roman(n)) == n
    for bad in ["IIII", "IC", "VX", ""]:
        try:
            from_roman(bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted {bad!r}")
    for _ in range(2000):
        n, base = rng.randint(-10**12, 10**12), rng.randint(2, 36)
        assert from_base(to_base(n, base), base) == n
        assert int(to_base(n, base), base) == n
    assert to_words(1001) == "one thousand and one"
    assert to_words(-52) == "minus fifty-two"
    assert humanize_bytes(1024 * 1024 - 20) == "1.0 MiB"
    assert clock(108_000) == "30:00:00"


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
