r"""Virtual environments: a private place to install packages for one project.

A Python installation has one shared `site-packages` folder. If project A needs
version 1 of a library and project B needs version 2, they cannot both install
into the same folder. A *virtual environment* (venv) solves that: it is a small
directory with its own `site-packages` and a `python` that points back at the
real interpreter. Packages installed while it is active land in the venv only.

    python -m venv .venv          create one (the usual name is .venv)
    source .venv/bin/activate     activate it (macOS / Linux)
    .venv\Scripts\activate        activate it (Windows)
    deactivate                    go back to the global Python

Two values tell you where you are:

    sys.base_prefix   the real installation Python was built from
    sys.prefix        the environment in use; differs from base_prefix in a venv

A venv is disposable. Never commit it to git; commit the list of requirements
instead and recreate the venv from that list.
"""

import sys
import sysconfig
from pathlib import Path


def in_virtualenv() -> bool:
    # Inside a venv, sys.prefix points at the venv and base_prefix at the
    # installation it was created from. Outside one, they are equal.
    return sys.prefix != sys.base_prefix


def where_am_i_demo() -> None:
    print(f"running inside a venv: {in_virtualenv()}")
    print(f"interpreter file name: {Path(sys.executable).name}")
    # purelib is the site-packages folder that `pip install` would write to.
    purelib = Path(sysconfig.get_paths()["purelib"])
    print(f"packages install into a folder named: {purelib.name}")
    # A plain install has no pyvenv.cfg beside it; that file marks a venv.
    has_cfg = (Path(sys.prefix) / "pyvenv.cfg").exists()
    print(f"pyvenv.cfg found at sys.prefix: {has_cfg}")


def main() -> None:
    where_am_i_demo()


if __name__ == "__main__":
    main()
