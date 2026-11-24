# Contributing to LearnPython

Thanks for helping grow the collection. This repo follows a few simple conventions so learners can browse it easily and so the git history stays useful as a learning artifact of its own.

## File conventions

1. **One concept per file.** If a topic can be split into two independent pieces, make two files.
2. **Every file is runnable.** Include a `main()` function guarded by `if __name__ == "__main__":` that demonstrates the code. A reader should be able to `python3 <path>` any file in the repo and see output.
3. **`basics/` files include teaching comments.** Explain *what* the code does and *why*, in plain English, for a first-time learner. Algorithm files stay clean — comment only when the *why* is non-obvious.
4. **Modern Python (3.12+).** Use type hints, f-strings, `match` statements, `dataclass`, and built-in generics (`list[int]`, not `List[int]`) where they make the code clearer.
5. **No dependencies.** Every sample runs against the standard library alone. If a sample truly needs a package, open an issue first.

## Packages (`*_kit`)

Each category folder may hold one small working package that wraps its single-file samples behind a clean API. The single files stay as they are; the package is the "put it together" lesson.

- Name it `<topic>_kit` (e.g. `sorts/sort_kit`). Layout: `__init__.py` (public API, `__all__`), one or two implementation modules, `__main__.py` (a demo that also self-checks and exits non-zero on failure), and a short `README.md`.
- Use relative imports inside the package. Run it from the repo root with `python3 -m sorts.sort_kit`.
- Standard library only, same as everything else. Type hints and a docstring on every public function.
- Add the package files in dependency order, one commit per file, and regenerate `DIRECTORY.md` last.

## Commit conventions

- **Small commits.** A file grows one idea at a time: the first commit adds the
  core idea with a runnable `main()`, and each later commit adds one more piece
  (a variant, an edge case, a self-check). Every commit must run on its own.
- **Commit message format:** `Add: <path> — <what it teaches>` for the first
  commit of a file, `Extend: <path> — <what this step adds>` for later ones.
  - Example: `Add: sorts/bubble_sort.py — iterative bubble sort with in-place swap`
  - Example: `Extend: basics/13_standard_library/regex_basics.py — capturing groups and named groups`
- Separate documentation commits use `docs: <path> — <what changed>`.

## The course: `basics/`

- Each chapter folder `NN_topic/` has a `README.md` listing its files **in
  reading order**. When you add a file, add it to that table where it belongs.
- Files are teaching material: a module docstring that explains the idea in
  plain English, comments on the *why*, and a demo whose output is easy to read.

## Exercises: `exercises/`

- One file per chapter, `chNN_<topic>.py`, with a matching
  `exercises/solutions/chNN_<topic>.py`.
- Each exercise is a stub that raises `NotImplementedError`, a docstring that
  states the task, and a `test_<name>(impl)` function full of asserts.
- The shared `report()` helper prints exactly one line per exercise:
  `[solved]`, `[not yet] <why>` or `[todo] not attempted`. It never crashes,
  and the file always exits 0.
- Solutions load the exercise file's tests with `runpy.run_path` instead of
  copying them, so the two can never drift apart. Commit the exercise file
  before its solutions file.
- Use only what the chapter (and earlier chapters) taught.

## Projects: `projects/`

- One complete program per file, built up over a few commits.
- The docstring says what it builds and has a `Uses:` list of chapters.
- Running the file with no arguments plays a scripted demo, because CI runs
  every file without input. An interactive mode may use `--play`.
- Add it to the table in `projects/README.md` with the chapter it needs.

## Naming

- Directories: `snake_case`, numeric-prefixed only inside `basics/` (to enforce reading order).
- Files: `snake_case.py`, descriptive over clever. `binary_search_recursive.py` beats `bsr.py`.

## Before opening a PR

- Run the file: `python3 <path>`. It must print something, exit 0, and not read from standard input.
- Run everything: `python3 .github/scripts/run_all.py`.
- Keep it PEP 8 clean (4-space indent, `snake_case`, ≤ 88 column soft limit).
- Update `DIRECTORY.md` if you added new files: `python3 .github/scripts/gen_directory.py`.
