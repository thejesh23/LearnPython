# LearnPython

> Everything you need to learn Python in one place: a 23-chapter course from `Hello, world!` to packaging, 121 exercises with solutions, 12 complete projects, and a library of 280+ runnable algorithm and deep-dive samples.

[![Python](https://img.shields.io/badge/Python-%5E3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Style: PEP 8](https://img.shields.io/badge/style-PEP%208-blue.svg)](https://peps.python.org/pep-0008/)

Every file in this repository is a self-contained lesson: open it, read it top to bottom, and run it with one command. Nothing to install except Python itself. There are no third-party packages anywhere.

---

## Table of contents

- [Why LearnPython?](#why-learnpython)
- [Quick start](#quick-start)
- [Where to start](#where-to-start)
- [How to study](#how-to-study)
- [The course (basics/)](#the-course-basics)
- [Exercises](#exercises)
- [Projects](#projects)
- [Going deeper](#going-deeper)
- [A taste of the code](#a-taste-of-the-code)
- [How this repo is organized](#how-this-repo-is-organized)
- [Repository conventions](#repository-conventions)
- [Contributing](#contributing)
- [Inspiration](#inspiration)
- [License](#license)

---

## Why LearnPython?

Most tutorials either bury you in features before you can write a program, or hand you a finished application with no explanation of its pieces. LearnPython takes a third path, **one concept per file**, and gives you the whole journey in one place:

- **Learn**: a numbered course in [`basics/`](basics/), with plain-English explanations in every file.
- **Practise**: an exercise file for every chapter in [`exercises/`](exercises/), which checks your answers and has worked solutions.
- **Build**: complete programs in [`projects/`](projects/) that combine many chapters.
- **Go deeper**: dense deep dives in [`advanced/`](advanced/) and 29 categories of classic algorithms.

Every file runs, and CI runs every one of them on Python 3.12 and 3.13 on each push.

## Quick start

1. **Install Python** from [python.org/downloads](https://www.python.org/downloads/). Any CPython `3.12` or newer works.
2. **Clone the repo:**

   ```bash
   git clone https://github.com/thejesh23/LearnPython.git
   cd LearnPython
   ```

3. **Run your first lesson:**

   ```bash
   python3 basics/00_hello_world/hello_world.py
   ```

That's the whole workflow. There is no build step, no virtualenv and no `pip install`. [DIRECTORY.md](DIRECTORY.md) lists every runnable file.

## Where to start

| You are... | Start at | Then |
|------------|----------|------|
| **New to programming** | [`basics/00_hello_world/`](basics/00_hello_world/) | Go through the chapters in order, doing each chapter's exercises before moving on. |
| **Coming from another language** (JavaScript, Java, C#, Go, Dart...) | [`basics/02_types/`](basics/02_types/) | Skim chapters 02–09 for Python's idioms (comprehensions, generators, decorators, context managers, `match`), then dig into 10–22. |
| **Already writing Python** | [`basics/15_typing/`](basics/15_typing/) or any chapter from 13 on | Fill gaps with the later chapters, the [projects](projects/) and [`advanced/`](advanced/). |
| **Preparing for interviews or CS classes** | The [algorithm categories](#going-deeper) | Each algorithm is one small, focused file that checks itself. |

## How to study

Each chapter follows the same loop:

1. **Read** the chapter's `README.md`. It lists the files in reading order.
2. **Run** each file and read it alongside its output. Change something and run it again.
3. **Practise** with the chapter's exercise file until every line says `[solved]`.
4. **Build** a project once you reach the chapter it needs. See the "Ready after" column in [`projects/`](projects/).
5. **Go deeper** with the chapter's links into `advanced/` and the algorithm folders, when you're curious.

## The course (`basics/`)

Each chapter folder has its own README with the reading order, the exercises, and links for going deeper.

### Part 1: Foundations

| # | Chapter | You'll learn |
|---|---------|--------------|
| 00 | [Hello, world](basics/00_hello_world/) | Running a script, `print`, the `__main__` guard |
| 01 | [Variables](basics/01_variables/) | Assignment, naming, constants by convention, unpacking |
| 02 | [Types](basics/02_types/) | `int`, `float`, `str`, `bool`, `None`, conversions, type hints, `Decimal` and `Fraction` |
| 03 | [Operators](basics/03_operators/) | Arithmetic, comparison, logic, identity and membership, the walrus |
| 04 | [Strings](basics/04_strings/) | Slicing, methods, f-strings, raw strings, text tools, Unicode and bytes |
| 05 | [Control flow](basics/05_control_flow/) | `if`, `for`, `while`, `break`/`continue`/`else`, `match` |
| 06 | [Functions](basics/06_functions/) | Parameters of every kind, docstrings, lambdas, higher-order functions, closures, decorators, recursion |
| 07 | [Collections](basics/07_collections/) | Lists, tuples, dicts, sets, comprehensions, sorting, copying, stacks and queues |
| 08 | [Iterators and generators](basics/08_iterators/) | The iterator protocol, `yield`, `itertools`, lazy pipelines, `yield from` and `send` |

### Part 2: Building real programs

| # | Chapter | You'll learn |
|---|---------|--------------|
| 09 | [Classes](basics/09_classes/) | Classes, properties, dunder methods, dataclasses, enums, inheritance vs composition, protocols, slots, descriptors, metaclasses |
| 10 | [Async](basics/10_async/) | `async`/`await`, tasks, async generators and queues, timeouts, running blocking code |
| 11 | [Errors](basics/11_errors/) | `try`/`except`/`else`/`finally`, raising, custom exceptions, exception groups, warnings, debugging |
| 12 | [Modules and I/O](basics/12_modules_io/) | Imports, `pathlib`, `with`, `contextlib`, JSON, CSV, config files |
| 13 | [The standard library](basics/13_standard_library/) | `collections`, `functools`, `datetime`, `re`, `logging` |
| 14 | [Testing](basics/14_testing/) | `assert`, doctest, `unittest`, `unittest.mock` |

### Part 3: Python in the real world

| # | Chapter | You'll learn |
|---|---------|--------------|
| 15 | [Typing](basics/15_typing/) | Generics (3.12 syntax), `TypedDict`, `Literal`, `Callable`, `@overload`, `NewType`, hints at runtime |
| 16 | [Threads and processes](basics/16_threads_and_processes/) | Threads, race conditions and locks, queues, thread and process pools, choosing a concurrency model |
| 17 | [The OS and the command line](basics/17_os_and_command_line/) | `argparse`, environment variables, `subprocess`, files and folders, exit codes and signals |
| 18 | [Data and storage](basics/18_data_and_storage/) | SQLite, pickle (and its dangers), binary data with `struct`, archives, hashing and secrets |
| 19 | [Networking](basics/19_networking/) | URLs, sockets, HTTP servers and clients, a JSON API client with retries |
| 20 | [Performance](basics/20_performance/) | `timeit`, `cProfile`, `tracemalloc`, choosing data structures, faster idioms |
| 21 | [Pythonic code](basics/21_pythonic_code/) | The Zen of Python, idiomatic loops, EAFP vs LBYL, common mistakes, style and PEP 8 |
| 22 | [Packaging and projects](basics/22_packaging_and_projects/) | Virtual environments, installing packages, `pyproject.toml`, project layout and tests |

## Exercises

[`exercises/`](exercises/) has one file per chapter, 121 tasks in all. Each task is a stub with a docstring and a test underneath:

```text
$ python3 exercises/ch07_collections.py
1. squares_of_evens                      [solved]
2. unique_in_order                       [not yet] unique_in_order(['b', 'a', 'b', 'c', 'a']) returned ['a', 'b', 'c'], expected ['b', 'a', 'c']
3. word_counts                           [todo] not attempted
```

Every exercise file has a matching file in [`exercises/solutions/`](exercises/solutions/) that runs the same tests against an idiomatic answer.

## Projects

[`projects/`](projects/) has twelve complete programs, from a quiz game and a text adventure to an expense tracker on SQLite and a URL shortener with its own web server. Each one lists the chapters it draws on, runs a scripted demo by default, and was built up commit by commit, so its history replays how it was made.

## Going deeper

- **[`advanced/`](advanced/)**: 38 dense single-file deep dives for readers who know the basics, such as descriptors, metaclasses, the GIL, weakrefs, bytecode, and a mini event loop.
- **Algorithms**: 29 categories, each with one algorithm per file and a `main()` that checks it. Each category also has a `*_kit` package that puts its samples together behind a clean API.

`arrays/` · `sorts/` · `searches/` · `strings/` · `maths/` · `recursion/` · `data_structures/` · `linked_lists/` · `trees/` · `matrix/` · `dynamic_programming/` · `graphs/` · `greedy/` · `backtracking/` · `bit_manipulation/` · `number_theory/` · `numeric/` · `geometry/` · `conversions/` · `ciphers/` · `crypto/` · `compression/` · `concurrency/` · `distributed/` · `machine_learning/` · `probabilistic/` · `parsers/` · `project_euler/` · `puzzles/`

## A taste of the code

**Your first Python program**, from `basics/00_hello_world/hello_world.py`:

```python
print("Hello, world!")
```

**Structural pattern matching**, from chapter 05:

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

**A generic stack**, using the 3.12 syntax from chapter 15:

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
├── basics/                 the course: chapters 00_ ... 22_, each with a README
├── exercises/              one practice file per chapter
│   └── solutions/          worked answers that run the same tests
├── projects/               complete programs that combine many chapters
├── advanced/               single-file deep dives
├── sorts/ graphs/ ...      29 algorithm categories, each with a *_kit package
├── DIRECTORY.md            flat index of every runnable file
├── CONTRIBUTING.md         file and commit conventions
├── LICENSE                 MIT
└── README.md               you are here
```

## Repository conventions

- **One concept per file.** If it can be split, split it.
- **Small commits.** A file grows across a few commits, one idea at a time, and every commit runs. `git log --follow <file>` replays how it was built.
- **Every file runs.** Each file has a `main()` you can run directly.
- **Zero dependencies.** Everything runs on the standard library alone.
- **`basics/` files teach.** Their comments explain the *what* and the *why*.
- **Algorithm files stay clean.** They only comment when the *why* is non-obvious.

Full details in [CONTRIBUTING.md](CONTRIBUTING.md).

## Contributing

New samples, exercises and projects are always welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) first. The short version:

1. One concept per file. If it can be split, split it.
2. Small commits. Message format: `Add: <path> — <one-line what it teaches>`.
3. Run the file before you submit it.
4. Update `DIRECTORY.md` when you add files (`python3 .github/scripts/gen_directory.py`).

## Inspiration

- [TheAlgorithms/Python](https://github.com/TheAlgorithms/Python): the model for the algorithm categories.
- [docs.python.org/3/tutorial](https://docs.python.org/3/tutorial/): the canonical reference for every language feature covered in `basics/`.
- [LearnDart](https://github.com/polyglot-learn/LearnDart): the sibling repository for Dart.

## License

Released under the [MIT License](LICENSE).
