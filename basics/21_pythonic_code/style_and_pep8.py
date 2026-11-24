"""Style and PEP 8 — writing code that other people (and future you) can read.

PEP 8 is Python's style guide. Code is read far more often than it is
written, so a shared style means anyone can open any Python file and find
their way around. The main points:

    naming     snake_case functions and variables, PascalCase classes,
               UPPER_CASE constants, a leading _ for "internal"
    layout     4-space indents, spaces around = and after commas, two blank
               lines between top-level definitions, short lines
    imports    one per line, at the top, grouped: standard library, then
               third-party, then your own modules, a blank line between
    docstrings a triple-quoted summary line on every public function,
               class and module (PEP 257)

Nobody checks these by hand any more. The usual tools (installed with pip,
not part of the standard library):

    ruff    a very fast linter: unused imports, bad names, likely bugs,
            import order. `ruff check .`  (`ruff check --fix .` repairs many)
    black   a formatter: rewrites layout so you never argue about it again.
            `black .`  (ruff also has a formatter: `ruff format .`)
    mypy    a type checker: reads your type hints and finds mismatches
            before the code runs. `mypy yourfile.py`
"""


# BEFORE: it works, but every line makes the reader stop and decode it.
def CalcStats( l,Flag = False ):
    t=0;n=0;M=None
    for i in range(len(l)):
        if l[i]!=None :
            t=t+l[i];n=n+1
            if M==None or l[i]>M : M=l[i]
    if Flag==True: return (t/n if n>0 else 0,M)
    else : return t/n if n>0 else 0


# AFTER: same behaviour, PEP 8 names and layout, a docstring, type hints.
def mean_and_max(
    values: list[float | None], *, include_max: bool = False
) -> float | tuple[float, float | None]:
    """Average the values that are not None, optionally with the maximum.

    Returns 0 for the mean when there is nothing to average.
    """
    present = [v for v in values if v is not None]
    mean = sum(present) / len(present) if present else 0
    if include_max:
        return mean, max(present, default=None)
    return mean


def before_after_demo() -> None:
    samples: list[list[float | None]] = [[3, None, 9, 6], [], [None, 2.5]]
    for data in samples:
        old = CalcStats(data, True)
        new = mean_and_max(data, include_max=True)
        print(f"{data!s:<18} old={old!s:<10} new={new!s:<10} same: {old == new}")
    # What changed: descriptive names; `is not None` instead of `!= None`;
    # no semicolons or one-line ifs; a keyword-only flag so callers write
    # include_max=True rather than a mysterious positional True; and the
    # loop over range(len(...)) became a comprehension.


def main() -> None:
    before_after_demo()


if __name__ == "__main__":
    main()
