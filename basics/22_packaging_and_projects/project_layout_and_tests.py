"""How a real project is laid out, and how its tests are found and run.

Most Python projects use the "src layout":

    shopcart-project/
        pyproject.toml          name, version, dependencies
        README.md
        src/
            shopcart/           the importable package
                __init__.py
                cart.py
        tests/
            __init__.py         empty; makes tests/ discoverable
            test_cart.py        one test module per source module

Why put the package under src/? Because the project root is not on the import
path, so `import shopcart` only works once the package is installed (or the
src folder is added on purpose). Tests then exercise the code the way users
will get it, and a forgotten file in the package shows up as a test failure
instead of silently working from your checkout.

`python -m unittest discover` walks a folder, imports every `test*.py` file,
and runs every TestCase it finds. pytest (a popular third-party runner) finds
the same tests with plain `pytest`.

This file builds such a project in a temporary folder and runs its tests in a
child process, exactly as you would from a terminal.
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


PROJECT = {
    "pyproject.toml": """\
[project]
name = "shopcart"
version = "0.1.0"
requires-python = ">=3.12"
""",
    "README.md": "# shopcart\n\nA tiny shopping cart.\n",
    "src/shopcart/__init__.py": "from shopcart.cart import Cart\n",
    "src/shopcart/cart.py": """\
class Cart:
    def __init__(self) -> None:
        self.items: dict[str, tuple[int, float]] = {}

    def add(self, name: str, price: float, qty: int = 1) -> None:
        if qty < 1:
            raise ValueError("qty must be at least 1")
        old_qty = self.items.get(name, (0, price))[0]
        self.items[name] = (old_qty + qty, price)

    def total(self) -> float:
        return round(sum(q * p for q, p in self.items.values()), 2)
""",
    # An empty __init__.py makes tests/ a package that discovery walks into.
    "tests/__init__.py": "",
    "tests/test_cart.py": """\
import unittest

from shopcart import Cart


class CartTests(unittest.TestCase):
    def test_empty_cart_costs_nothing(self) -> None:
        self.assertEqual(Cart().total(), 0)

    def test_adding_same_item_twice_adds_quantity(self) -> None:
        cart = Cart()
        cart.add("tea", 2.50)
        cart.add("tea", 2.50, qty=2)
        self.assertEqual(cart.total(), 7.50)

    def test_zero_quantity_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Cart().add("tea", 2.50, qty=0)
""",
}


def build_project(root: Path, files: dict[str, str]) -> None:
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)


def print_tree(root: Path) -> None:
    for path in sorted(root.rglob("*")):
        if "__pycache__" in path.parts:
            continue
        depth = len(path.relative_to(root).parts) - 1
        suffix = "/" if path.is_dir() else ""
        print(f"  {'    ' * depth}{path.name}{suffix}")


def layout_demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        build_project(Path(tmp), PROJECT)
        print("shopcart-project/")
        print_tree(Path(tmp))


def run_tests(root: Path, src_on_path: bool) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    if src_on_path:
        # What `pip install -e .` would arrange for us: make src/ importable.
        env["PYTHONPATH"] = str(root / "src")
    else:
        env.pop("PYTHONPATH", None)
    # discover starts in the current folder; -v prints one line per test.
    command = [sys.executable, "-m", "unittest", "discover", "-v"]
    return subprocess.run(command, cwd=root, env=env, capture_output=True,
                          text=True)


def tidy_output(text: str) -> list[str]:
    # unittest reports on stderr; drop the timing so the output is stable.
    text = re.sub(r" in \d+\.\d+s", "", text)
    # Each test is named twice ("test_x (tests.test_cart...)"); keep the short one.
    text = re.sub(r" \(tests\.[\w.]+\)", "", text)
    return [line for line in text.splitlines() if line.strip()]


def discover_demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        build_project(root, PROJECT)

        print("$ python -m unittest discover -v   (src/ not on the path)")
        result = run_tests(root, src_on_path=False)
        errors = [line for line in tidy_output(result.stderr) if "Error:" in line]
        for line in (errors[0], errors[-1]):  # what failed, and why
            print(f"  {line}")
        print(f"  exit code {result.returncode}: the package is not installed")

        print("$ PYTHONPATH=src python -m unittest discover -v")
        result = run_tests(root, src_on_path=True)
        for line in tidy_output(result.stderr):
            print(f"  {line}")
        print(f"  exit code {result.returncode}")


def main() -> None:
    layout_demo()
    print()
    discover_demo()


if __name__ == "__main__":
    main()
