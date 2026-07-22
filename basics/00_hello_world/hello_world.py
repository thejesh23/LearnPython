"""Your first Python program.

`print` writes text to the terminal. Python runs a file top to bottom, so
this single line is the whole program.

The `if __name__ == "__main__":` guard below is the Python convention for
"run this only when the file is executed directly, not when it is imported
by another file". Every file in this repo uses it, so you can both run a
file and reuse its functions elsewhere.
"""


def main() -> None:
    print("Hello, world!")


if __name__ == "__main__":
    main()
