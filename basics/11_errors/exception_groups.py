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


def main() -> None:
    group_demo()


if __name__ == "__main__":
    main()
