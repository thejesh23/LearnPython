"""Installing packages with pip, pinning them, and checking what is installed.

Code other people publish lives on PyPI (the Python Package Index). `pip`
downloads a package from there and unpacks it into the active environment's
`site-packages`. Always do this inside a virtual environment (see
virtual_environments.py) so each project keeps its own set.

    python -m pip install requests          latest version
    python -m pip install "requests>=2.31"  any version from 2.31 up
    python -m pip install -r requirements.txt
    python -m pip freeze > requirements.txt record exact versions
    python -m pip list                      what is installed

Use `python -m pip` rather than a bare `pip`: it guarantees pip installs into
the same Python you will run.

Version specifiers say which versions are acceptable:

    ==2.31.0   exactly this one (a "pin")
    >=2.31     this or newer
    <3         anything before 3.0
    !=2.30.1   anything but this one
    ~=2.31     "compatible release": >=2.31 and <3.0

The package you install (the *distribution*, e.g. "PyYAML") can have a
different name from the module you import ("yaml"). `importlib.metadata`
reads what is installed without importing it.
"""

import re
from importlib import metadata


def parse_version(text: str) -> tuple[int, ...]:
    # Real versions can be "2.0rc1" or "1.0.post2"; pip uses the `packaging`
    # library for those. Plain dotted numbers are enough to learn the rules.
    return tuple(int(part) for part in text.split("."))


def satisfies(version: str, spec: str) -> bool:
    match = re.fullmatch(r"(==|!=|>=|<=|~=|<|>)\s*([\d.]+)", spec.strip())
    if match is None:
        raise ValueError(f"bad specifier: {spec!r}")
    op, wanted = match.groups()
    have, want = parse_version(version), parse_version(wanted)
    # Pad to the same length so (2, 31) compares like (2, 31, 0).
    width = max(len(have), len(want))
    have += (0,) * (width - len(have))
    padded = want + (0,) * (width - len(want))
    match op:
        case "==":
            return have == padded
        case "!=":
            return have != padded
        case ">=":
            return have >= padded
        case "<=":
            return have <= padded
        case ">":
            return have > padded
        case "<":
            return have < padded
        case _:  # "~=": at least `want`, same release series
            return have >= padded and have[: len(want) - 1] == want[:-1]


def specifier_demo() -> None:
    specs = ["==2.31.0", ">=2.31", "<3", "!=2.30.1", "~=2.31"]
    versions = ["2.30.1", "2.31.0", "2.32.3", "3.0.0"]
    print("which versions each specifier accepts:")
    print(f"{'':10}" + "".join(f"{v:>9}" for v in versions))
    for spec in specs:
        row = "".join(f"{'yes' if satisfies(v, spec) else '-':>9}" for v in versions)
        print(f"{spec:10}{row}")


def installed() -> dict[str, str]:
    """Map each installed distribution name to its version."""
    found = {}
    for dist in metadata.distributions():
        name = dist.metadata["Name"]
        if name:  # a broken install can have empty metadata
            found[name] = dist.version
    return found


def installed_demo() -> None:
    dists = installed()
    print(f"{len(dists)} distributions installed in this environment")
    if not dists:
        print("  (a fresh venv has none; try `python -m pip install requests`)")
    for name in sorted(dists, key=str.lower)[:5]:
        print(f"  {name}=={dists[name]}")

    # version() looks up one distribution; a missing one raises an error.
    for name in ["pip", "surely-not-installed-pkg"]:
        try:
            print(f"{name} version: {metadata.version(name)}")
        except metadata.PackageNotFoundError:
            print(f"{name}: not installed")

    # Distribution name vs import name, e.g. PyYAML installs a module `yaml`.
    differ = [(mod, dist[0]) for mod, dist in
              metadata.packages_distributions().items()
              if dist and mod.lower() != dist[0].lower() and not mod.startswith("_")]
    for module, dist in sorted(differ)[:3]:
        print(f"  import {module}  comes from distribution {dist}")


def main() -> None:
    specifier_demo()
    print()
    installed_demo()


if __name__ == "__main__":
    main()
