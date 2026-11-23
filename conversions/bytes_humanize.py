"""Human-readable byte sizes in SI (kB = 1000) and IEC (KiB = 1024) units.

Two conventions are in everyday use and they disagree: a "500 GB" disk sold
in SI units shows up as about 465 GiB in an operating system that counts in
IEC units. The algorithm is the same for both: divide by the base until the
value drops under it, counting steps to pick the unit.

The subtle bug is rounding. 1023.96 KiB formatted to one decimal reads
"1024.0 KiB" when it should have become "1.0 MiB". The fix is to round first
and then check whether the rounded value reached the base. Parsing goes the
other way and must accept either convention by its suffix.
"""

import re

SI = ["B", "kB", "MB", "GB", "TB", "PB", "EB"]
IEC = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB"]


def humanize(n: int, si: bool = False, places: int = 1) -> str:
    if n < 0:
        return "-" + humanize(-n, si, places)
    base, units = (1000, SI) if si else (1024, IEC)
    if n < base:
        return f"{n} B"
    value = float(n)
    i = 0
    while i < len(units) - 1 and round(value, places) >= base:
        value /= base
        i += 1
    return f"{value:.{places}f} {units[i]}"


def humanize_naive(n: int, si: bool = False) -> str:
    base, units = (1000, SI) if si else (1024, IEC)
    value, i = float(n), 0
    while value >= base and i < len(units) - 1:
        value /= base
        i += 1
    return f"{value:.1f} {units[i]}"


PATTERN = re.compile(r"\s*([0-9.]+)\s*([kKMGTPE]?i?)B?\s*$")


def parse(text: str) -> int:
    match = PATTERN.match(text)
    if not match:
        raise ValueError(f"cannot parse size: {text!r}")
    number, prefix = float(match[1]), match[2]
    if not prefix:
        return round(number)
    base = 1024 if prefix.endswith("i") else 1000
    power = "KMGTPE".index(prefix[0].upper()) + 1
    return round(number * base**power)


def main() -> None:
    for n in [0, 999, 1000, 1024, 1536, 10**6, 2**20, 500 * 10**9, 2**40 + 1]:
        print(f"{n:>15,}  SI {humanize(n, si=True):>10}  IEC {humanize(n):>10}")

    print("\nrounding at the boundary:")
    edge = 1024 * 1024 - 20
    print(f"  naive   {humanize_naive(edge)}")
    print(f"  correct {humanize(edge)}")

    print("\nthe disk-size surprise:")
    print(f"  500 GB on the box = {humanize(parse('500 GB'))} in the OS")

    for text in ["1.5 KiB", "1.5 kB", "2 GiB", "750", "3.2 TB"]:
        print(f"  parse({text!r}) = {parse(text):,}")

    agree = all(abs(parse(humanize(n)) - n) <= n * 0.05 + 1
                for n in range(0, 10**7, 9973))
    print(f"\nparse(humanize(n)) within 5% across a sweep: {agree}")


if __name__ == "__main__":
    main()
