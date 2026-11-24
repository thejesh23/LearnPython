"""Exception groups, `except*`, and notes on exceptions (Python 3.11+).

Sometimes several things fail at once: three of ten parallel downloads, or
five fields of a form. Raising only the first error hides the rest.
`ExceptionGroup` bundles several exceptions into one, and `except*` handles
the matching ones by type while letting the others carry on up the stack.

`add_note()` attaches extra context to any exception. The note is printed
under the error message in the traceback, which is handy when you re-raise
an error and want to say what you were doing at the time.
"""


def validate(form: dict[str, str]) -> None:
    errors: list[Exception] = []
    if not form.get("name"):
        errors.append(ValueError("name is required"))
    if not form.get("age", "").isdigit():
        errors.append(TypeError("age must be a whole number"))
    if "@" not in form.get("email", ""):
        errors.append(ValueError("email needs an @"))
    if errors:
        raise ExceptionGroup("form is invalid", errors)


def group_demo() -> None:
    try:
        validate({"name": "", "age": "ten", "email": "ana.example.com"})
    except* ValueError as group:
        # group is an ExceptionGroup holding only the ValueErrors.
        for err in group.exceptions:
            print(f"value problem: {err}")
    except* TypeError as group:
        for err in group.exceptions:
            print(f"type problem: {err}")


def split_demo() -> None:
    # except* that handles only some types re-raises a smaller group with
    # the rest, so no failure is silently lost.
    try:
        try:
            raise ExceptionGroup("batch", [KeyError("x"), OSError("disk full")])
        except* KeyError:
            print("handled the KeyError")
    except ExceptionGroup as rest:
        print(f"still unhandled: {rest.exceptions!r}")


def load_settings(lines: list[str]) -> dict[str, int]:
    settings: dict[str, int] = {}
    for number, line in enumerate(lines, start=1):
        key, value = line.split("=")
        try:
            settings[key] = int(value)
        except ValueError as exc:
            exc.add_note(f"while reading line {number}: {line!r}")
            raise
    return settings


def notes_demo() -> None:
    try:
        load_settings(["width=80", "height=tall"])
    except ValueError as exc:
        print(f"error: {exc}")
        for note in exc.__notes__:
            print(f"note:  {note}")


def main() -> None:
    group_demo()
    print()
    split_demo()
    print()
    notes_demo()


if __name__ == "__main__":
    main()
