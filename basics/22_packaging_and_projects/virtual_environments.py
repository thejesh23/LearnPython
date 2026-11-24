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

import os
import subprocess
import sys
import sysconfig
import tempfile
import venv
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


def venv_python(env_dir: Path) -> Path:
    # Windows puts executables in Scripts\, everything else in bin/.
    if os.name == "nt":
        return env_dir / "Scripts" / "python.exe"
    return env_dir / "bin" / "python"


def create_venv_demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        env_dir = Path(tmp) / ".venv"
        # --without-pip skips installing pip, which keeps this fast and offline.
        subprocess.run([sys.executable, "-m", "venv", "--without-pip", str(env_dir)],
                       check=True)
        print("created .venv containing:")
        for item in sorted(env_dir.iterdir()):
            kind = "dir " if item.is_dir() else "file"
            print(f"  {kind} {item.name}")

        # pyvenv.cfg is how the venv's python finds the real installation.
        cfg = (env_dir / "pyvenv.cfg").read_text()
        keys = [line.split("=")[0].strip() for line in cfg.splitlines() if "=" in line]
        print(f"pyvenv.cfg keys: {keys}")

        # Ask the venv's own interpreter where it lives.
        code = "import sys; print(sys.prefix != sys.base_prefix)"
        result = subprocess.run([str(venv_python(env_dir)), "-c", code],
                                capture_output=True, text=True, check=True)
        print(f"the venv's python says it is in a venv: {result.stdout.strip()}")


def env_builder_demo() -> None:
    # The venv module can do the same thing from Python code.
    with tempfile.TemporaryDirectory() as tmp:
        env_dir = Path(tmp) / "env"
        venv.EnvBuilder(with_pip=False).create(env_dir)
        scripts = venv_python(env_dir).parent
        print(f"EnvBuilder made {scripts.name}/ with an activate script: "
              f"{any(p.name.startswith('activate') for p in scripts.iterdir())}")

        # "Activating" is only a shell convenience: it puts the venv's bin/
        # first on PATH (and sets VIRTUAL_ENV) so that typing `python` finds
        # the venv's interpreter. We can do the same by editing PATH ourselves.
        env = dict(os.environ, VIRTUAL_ENV=str(env_dir))
        env["PATH"] = str(scripts) + os.pathsep + env.get("PATH", "")
        code = ("import os, sys; "
                "print(os.path.samefile(sys.prefix, os.environ['VIRTUAL_ENV']))")
        result = subprocess.run(["python", "-c", code], env=env,
                                capture_output=True, text=True, check=True)
        print(f"`python` on the new PATH runs the venv: {result.stdout.strip()}")
    print("tip: you can skip activation and call .venv/bin/python directly")


def main() -> None:
    where_am_i_demo()
    print()
    create_venv_demo()
    print()
    env_builder_demo()


if __name__ == "__main__":
    main()
