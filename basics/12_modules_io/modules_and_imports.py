"""Modules, packages, and imports.

Every `.py` file is a module. Importing one *executes it once*, top to bottom,
and caches the result in `sys.modules` — which is why a second import of the
same module is free, and why top-level side effects run exactly once.

`import x` binds the module object; `from x import y` binds the name directly.
Prefer the first for clarity when the origin matters (`json.dumps` reads better
than a bare `dumps`).

Avoid `from x import *`: it hides where names came from and can silently
shadow your own.
"""

import json  # module object
import sys
from math import pi, sqrt  # names bound directly
from pathlib import Path as FsPath  # aliased on import


def main() -> None:
    print(f"json.dumps  -> {json.dumps({'a': 1})}")
    print(f"sqrt(16)    -> {sqrt(16)}, pi ~= {pi:.5f}")
    print(f"aliased     -> {FsPath('/tmp/example.txt').suffix}")

    # A module is an object with attributes.
    print(f"json is a {type(json).__name__} loaded from {FsPath(json.__file__).name}")
    print(f"cached in sys.modules: {'json' in sys.modules}")

    # __name__ is "__main__" when run directly, the module name when imported.
    print(f"__name__ = {__name__!r}")

    # Where imports are searched, in order.
    print("sys.path[0] is the script's own directory:")
    print(f"  {sys.path[0]}")
    print(f"  ...plus {len(sys.path) - 1} more entries (stdlib, site-packages)")

    # Import machinery, and how a missing module reports itself.
    try:
        import definitely_not_a_real_module  # noqa: F401
    except ModuleNotFoundError as exc:
        print(f"ModuleNotFoundError: {exc}")

    # A package is a directory of modules; `from pkg import mod` works because
    # Python treats the directory as a namespace. `__init__.py` (optional
    # since 3.3) is the place to curate a package's public surface.
    print("package layout:")
    print("  mypkg/__init__.py   -> re-export the public API here")
    print("  mypkg/core.py       -> import as `from mypkg import core`")
    print("  relative imports (`from . import core`) work inside a package only")


if __name__ == "__main__":
    main()
