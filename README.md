# LearnPython

> A hands-on collection of small, runnable Python programs — from your first `Hello, world!` to classic algorithms — written for two audiences at once.

[![Python](https://img.shields.io/badge/Python-%5E3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Style: PEP 8](https://img.shields.io/badge/style-PEP%208-blue.svg)](https://peps.python.org/pep-0008/)

Companion to [LearnDart](https://github.com/polyglot-learn/LearnDart), inspired by [TheAlgorithms/Python](https://github.com/TheAlgorithms/Python). Every file in this repository is a self-contained lesson: you can open it, read it top-to-bottom, and run it with a single command.

---

## Table of contents

- [Why LearnPython?](#why-learnpython)
- [Who this is for](#who-this-is-for)
- [Quick start](#quick-start)
- [The learning path (basics/)](#the-learning-path-basics)
- [Algorithm categories](#algorithm-categories)
- [A taste of the code](#a-taste-of-the-code)
- [How this repo is organized](#how-this-repo-is-organized)
- [Repository conventions](#repository-conventions)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Inspiration](#inspiration)
- [License](#license)

---

## Why LearnPython?

Most language tutorials fall into one of two traps: they either bury you in features before you can write a program, or they hand you a giant final application with no explanation of the pieces. LearnPython takes a third path — **one concept per file, one file per commit**. You can read the code, the comments, and (if you want) the git history and see exactly how the language was introduced, in order.

- **Read it as a book** — walk through `basics/` in order, no setup beyond installing Python.
- **Read it as a reference** — jump straight to `sorts/`, `graphs/`, `dynamic_programming/`, etc. when you need a clean Python implementation of a classic algorithm.
- **Read it as a git log** — every commit is atomic and titled `Add: <path> — <what it teaches>`.

## Who this is for

| Audience | Where to start | What you'll get |
|----------|----------------|-----------------|
| **Non-programmers** learning to code for the first time | [`basics/00_hello_world/`](basics/00_hello_world/) | Files are numbered `00`, `01`, `02`... so you always know the next step. Each `basics/` file has plain-English comments that explain *what* the code does and *why*. |
| **Programmers** coming from Dart, JavaScript, Go, Java, C# or similar | [`basics/02_types/`](basics/02_types/), then the algorithm categories | Skim the `basics/` folders for Python-specific idioms (duck typing, comprehensions, generators, decorators, context managers, `match`), then dive into idiomatic Python implementations of algorithms you already know. |
| **CS students** looking for clean reference implementations | Any algorithm category below | Every algorithm is a small, focused file with a `main()` that exercises it. No frameworks, no packages — just Python and its standard library. |

## Quick start

1. **Install Python** — see [python.org/downloads](https://www.python.org/downloads/). Any CPython `3.12` or newer works (CI runs 3.12 and 3.13).
2. **Clone the repo:**

   ```bash
   git clone https://github.com/thejesh23/LearnPython.git
   cd LearnPython
   ```

3. **Run any file:**

   ```bash
   python3 basics/00_hello_world/hello_world.py
   ```

That's the whole workflow. There is no build step, no virtualenv, no `pip install` — the repo has zero third-party dependencies.

## The learning path (`basics/`)

Follow the numbered folders in order. Inside each folder, read the files in alphabetical order.

| # | Folder | You'll learn |
|---|--------|--------------|
| 00 | `00_hello_world/` | Running a script, `print`, the `__main__` guard |
| 01 | `01_variables/` | Assignment, naming, constants by convention, unpacking |
| 02 | `02_types/` | `int`, `float`, `str`, `bool`, `None`, type hints |
| 03 | `03_operators/` | Arithmetic, comparison, logical, identity/membership, walrus |
| 04 | `04_strings/` | f-strings, slicing, common methods, multiline/raw strings |
| 05 | `05_control_flow/` | `if`/`elif`/`else`, `for`, `while`, `break`/`continue`/`else`, `match` |
| 06 | `06_functions/` | Defaults, `*args`/`**kwargs`, keyword-only and positional-only, lambdas, closures, decorators |
| 07 | `07_collections/` | `list`, `tuple`, `dict`, `set`, comprehensions, slicing |
| 08 | `08_iterators/` | Iterables, generators, `yield`, `itertools` |
| 09 | `09_classes/` | Attributes, `__init__`, class and static methods, dunder methods, inheritance, `dataclass`, `Enum` |
| 10 | `10_async/` | `async`/`await`, `asyncio.gather`, async generators |
| 11 | `11_errors/` | `try`/`except`/`else`/`finally`, raising, custom exceptions, exception groups |
| 12 | `12_modules_io/` | Imports, `pathlib`, context managers, JSON, CSV |
| 13 | `13_standard_library/` | `collections`, `functools`, `datetime`, `re`, `logging` |
| 14 | `14_testing/` | `assert`, doctest, `unittest`, `unittest.mock` |

## Algorithm categories

Each category holds one algorithm per file, each with a runnable `main()`:

`arrays/` · `sorts/` · `searches/` · `strings/` · `maths/` · `recursion/` · `data_structures/` · `dynamic_programming/` · `graphs/` · `greedy/` · `backtracking/` · `bit_manipulation/` · `number_theory/` · `geometry/` · `ciphers/` · `crypto/` · `compression/` · `concurrency/` · `distributed/` · `machine_learning/` · `probabilistic/` · `parsers/` · `project_euler/` · `puzzles/` · `conversions/` · `matrix/` · `linked_lists/` · `trees/`

See [DIRECTORY.md](DIRECTORY.md) for a flat index of every file.

## A taste of the code

**Your first Python program** — `basics/00_hello_world/hello_world.py`:

```python
print("Hello, world!")
```

**Python 3.10 structural pattern matching:**

```python
def describe(n: int) -> str:
    match n:
        case 0:
            return "zero"
        case 1 | 2 | 3:
            return "small"
        case _ if n < 0:
            return "negative"
        case _:
            return "large or unusual"
```

**A generic stack:**

```python
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, value: T) -> None:
        self._items.append(value)

    def pop(self) -> T:
        return self._items.pop()
```

## How this repo is organized

```text
LearnPython/
├── basics/                 numbered teaching folders 00_ ... 14_
│   ├── 00_hello_world/
│   ├── 01_variables/
│   └── ...
├── sorts/                  one algorithm per file
├── searches/
├── data_structures/
├── maths/
├── strings/
├── DIRECTORY.md            flat index of every .py file
├── CONTRIBUTING.md         file and commit conventions
├── LICENSE                 MIT
└── README.md               you are here
```

## Repository conventions

- **One concept per file.** Splittable? Split it.
- **One file per commit, one commit per pull request.** The git history *is* the reading order, and every change stays small enough to review at a glance.
- **Every file runs.** No file exists without a `main()` you can execute directly.
- **Zero dependencies.** Every sample runs against the standard library alone.
- **`basics/` files teach.** They have prose comments explaining the *what* and the *why*.
- **Algorithm files stay clean.** They only comment when the *why* is non-obvious.
- **Iterative + recursive = two commits.** Same algorithm, two shapes — they get their own files.

Full details in [CONTRIBUTING.md](CONTRIBUTING.md).

## Roadmap

More samples land in later sessions. Planned expansions mirror [LearnDart](https://github.com/polyglot-learn/LearnDart): the full `basics/` path first, then sorts, searches, data structures, graphs, DP, and the advanced categories (crypto, compression, distributed, probabilistic).

## Contributing

New samples are always welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) first — the short version:

1. One concept per file. Splittable? Split it.
2. One file per commit, one commit per PR. Message format: `Add: <path> — <one-line what it teaches>`.
3. Run the file before you submit it.
4. Update `DIRECTORY.md` when you add files.

## Inspiration

- [LearnDart](https://github.com/polyglot-learn/LearnDart) — the sibling repository this one mirrors.
- [TheAlgorithms/Python](https://github.com/TheAlgorithms/Python) — the model for the algorithm categories.
- [docs.python.org/3/tutorial](https://docs.python.org/3/tutorial/) — canonical reference for every language feature covered in `basics/`.

## License

Released under the [MIT License](LICENSE).
